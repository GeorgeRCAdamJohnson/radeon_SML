@echo off
echo Starting Radeon AI Knowledge Base Server...
echo.
echo Make sure you have the required dependencies installed:
echo pip install fastapi uvicorn pydantic
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python server.py
pause