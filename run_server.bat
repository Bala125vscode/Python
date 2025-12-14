@echo off
cd /d "%~dp0"
echo Working directory set to: %CD%
echo Starting LaTeX Converter Server...
uvicorn app.main:app --reload
pause
