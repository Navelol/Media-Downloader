@echo off
echo Starting Media Downloader...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run "install.bat" first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run the application
call .venv\Scripts\activate.bat
python src\media-downloader.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    pause
)
