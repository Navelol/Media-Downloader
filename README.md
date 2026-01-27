# Media Downloader

A simple GUI application for downloading media content using yt-dlp.

## Features

- Download videos in multiple formats: MP4, MKV, WebM, AVI, MOV
- Download audio in multiple formats: MP3, M4A, WAV, FLAC, Opus
- Real-time progress tracking with speed and ETA
- Support for single videos or playlists
- Clean, easy-to-use interface
- Cancel downloads at any time

## Requirements

- Python 3.7+
- FreeSimpleGUI
- yt-dlp
- certifi

## Installation

### Easy Installation (Windows - Recommended)

1. **Download this repository:**
   - Click the green "Code" button → "Download ZIP"
   - Extract the ZIP file to a folder of your choice

2. **Install Python** (if you don't have it):
   - Download from [python.org](https://www.python.org/downloads/)
   - **Important:** Check "Add Python to PATH" during installation

3. **Run the installer:**
   - Double-click `install.bat`
   - Wait for it to finish (this sets up everything automatically)

4. **Launch the application:**
   - Double-click `run.bat` anytime you want to use the app

That's it! No command line knowledge needed.

---

### Manual Installation (Mac/Linux or Advanced Users)

1. Clone this repository:
```bash
git clone https://github.com/Navelol/Media-Downloader.git
cd Media-Downloader
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```
*Note: If you get an execution policy error, run:*
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

You should see `(.venv)` at the beginning of your command prompt when the virtual environment is activated.

## Usage

### Easy Launch (Windows)
Simply double-click `run.bat` - the application will start automatically!

### Manual Launch
If you installed manually or are on Mac/Linux:

1. Activate your virtual environment (if not already active)
2. Run the application:
```bash
python src/media-downloader.py
```

### Using the Application

1. Paste a video URL
2. Choose a save location
3. Select download type (Video or Audio Only)
4. Choose your desired format from the dropdown
5. Click Download

**Available Formats:**
- **Video:** MP4, MKV, WebM, AVI, MOV
- **Audio:** MP3, M4A, WAV, FLAC (lossless), Opus

## Legal Disclaimer

**IMPORTANT: This tool is provided for educational and personal use only.**

- You are responsible for ensuring you have the legal right to download any content
- Only download content that you own, have permission to download, or that is in the public domain
- Respect copyright laws and the terms of service of the platforms you're downloading from
- The developers of this tool are not responsible for any misuse or legal consequences resulting from the use of this software
- This tool should not be used to infringe on anyone's intellectual property rights

**By using this software, you agree to use it responsibly and in compliance with all applicable laws.**

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is not affiliated with, endorsed by, or connected to any video platform or streaming service. It is an independent tool that uses publicly available libraries.
