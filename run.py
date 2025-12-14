
import os
import sys
import uvicorn

if __name__ == "__main__":
    # Get the directory of this script (project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure this directory is in sys.path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Change working directory to project root (important for templates/static files)
    os.chdir(project_root)
    print(f"Working directory set to: {os.getcwd()}")
    
    # Run Uvicorn
    # reload_dirs needs to be set to ensure it watches the right place if CWD was different originally
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true": # unexpected logic for uvicorn reloader? 
        # Uvicorn reloader spawns a subprocess. We only want to open browser once.
        # Simple Timer might open it twice if reloader restarts?
        # Actually, let's just use a simple timer. If it opens twice on code change it's annoying but acceptable for now.
        # Better: check if we can detect if it's the main process.
        pass

    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open("http://127.0.0.1:8000")
        
    Timer(1.5, open_browser).start()

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[project_root])
