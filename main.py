from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import difflib
import zipfile
import io
import os

import sys
import os

# Allow running main.py directly for debugging, or catch it to warn user
if __name__ == "__main__":
    if "app" not in os.getcwd(): # heuristic
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    else:
        sys.path.append(os.path.abspath('..'))

from app.converter import LatexConverter

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
converter = LatexConverter()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert", response_class=HTMLResponse)
async def convert_code(request: Request, code: str = Form(...)):
    converted_code = converter.convert(code)
    
    # Generate HTML diff
    diff_generator = difflib.HtmlDiff()
    # splitlines(keepends=True) needed? HtmlDiff expects lists of strings
    original_lines = code.splitlines()
    converted_lines = converted_code.splitlines()
    
    diff_html = diff_generator.make_table(
        original_lines, 
        converted_lines, 
        context=True, 
        numlines=5
    )
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "original_code": code,
        "converted_code": converted_code,
        "diff_html": diff_html
    })

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read file content
    content_bytes = await file.read()
    try:
        content_str = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return Response("Error: File must be UTF-8 encoded.", status_code=400)
    
    # Convert
    try:
        converted_str = converter.convert(content_str)
    except Exception as e:
        import traceback
        with open("debug_error.log", "w") as f:
            f.write(traceback.format_exc())
        return Response(f"Internal Error: {str(e)}", status_code=500)
    
    # Generate Diff
    diff_generator = difflib.HtmlDiff()
    diff_html = diff_generator.make_file(
        content_str.splitlines(),
        converted_str.splitlines(),
        fromdesc='Original',
        todesc='Converted',
        context=True,
        numlines=5
    )
    
    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Add converted tex
        # Sanitize filename?
        original_name = file.filename or "document.tex"
        name_root, ext = os.path.splitext(original_name)
        new_name = f"{name_root}_converted{ext}"
        zip_file.writestr(new_name, converted_str)
        
        # Add diff html
        zip_file.writestr("diff.html", diff_html)



    # Also save to local Downloads folder as requested
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path = os.path.join(downloads_path, f"{name_root}_converted_package.zip")
        with open(save_path, "wb") as f:
            f.write(zip_buffer.getvalue())
        print(f"Saved converted file to: {save_path}")
    except Exception as e:
        print(f"Could not save to Downloads folder: {e}")

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=converted_files.zip"}
    )

if __name__ == "__main__":
    import uvicorn
    print("Starting server via main.py...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
