# Media Downloader

A simple GUI application for downloading media content using yt-dlp.

## Features

- Download videos in MP4 format or audio in MP3 format
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
- Windows: `.\.venv\Scripts\Activate.ps1`
- Mac/Linux: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install FreeSimpleGUI yt-dlp certifi
```

## Usage

Run the application:
```bash
python src/media-downloader.py
```

1. Paste a video URL
2. Choose a save location
3. Select your desired format (MP4 or MP3)
4. Click Download

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
