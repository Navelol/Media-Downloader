@echo off

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run "install.bat" first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run the application without console window
start "" /B ".venv\Scripts\pythonw.exe" "src\media-downloader.py"

REM Exit immediately (terminal closes)
exit