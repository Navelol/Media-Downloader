#!/usr/bin/env python3
import os
import threading
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import FreeSimpleGUI as sg
import yt_dlp


# Global flag and thread handle for cancellation
cancel_flag = False
worker_thread = None


def download(url: str, output_dir: str, audio_only: bool = False, output_format: str = "mp4", no_playlist: bool = False, window=None) -> None:
    """
    Download media from URL using yt-dlp.
    Sends progress updates to the GUI window.
    """
    global cancel_flag

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError("Please enter a valid URL starting with http:// or https://")

    # Validate output directory
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Cannot create output directory: {e}")

    outtmpl = os.path.join(
        output_dir,
        "%(title)s-%(id)s.%(ext)s",
    )

    def progress_hook(d):
        """Called frequently by yt-dlp during download to report progress."""
        if cancel_flag:
            raise yt_dlp.utils.DownloadError("Download cancelled by user")
        
        if window and d['status'] == 'downloading':
            # Extract progress information
            percent = d.get('_percent_str', 'N/A').strip()
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', 'N/A').strip()
            
            # Send progress update to GUI
            window.write_event_value('-PROGRESS-', {
                'percent': percent,
                'speed': speed,
                'eta': eta,
                'filename': d.get('filename', 'Unknown')
            })
        
        elif window and d['status'] == 'finished':
            filename = d.get('filename', 'file')
            window.write_event_value('-PROGRESS-', {
                'status': 'finished',
                'filename': filename
            })

    ydl_opts = {
        "outtmpl": outtmpl,
        "ignoreerrors": False,  # Changed to False to catch errors properly
        "noplaylist": no_playlist,
        "progress_hooks": [progress_hook],
        "quiet": False,
        "no_warnings": False,
    }

    if audio_only:
        # Audio extraction with specified format
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "192" if output_format == "mp3" else "0",  # 0 = best quality for lossless
            }],
        })
    else:
        # Video download with specified format
        ydl_opts.update({
            "format": "bv*+ba/best",
            "merge_output_format": output_format,  # Force specific container format
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def start_download_in_thread(url, folder, audio_only, output_format, no_playlist, window):
    """
    Run download() in a separate thread so the GUI stays responsive.
    When done (success or error), send an event back to the window.
    """
    global cancel_flag
    cancel_flag = False

    try:
        download(url, folder, audio_only, output_format, no_playlist, window)
        window.write_event_value("-DOWNLOAD_DONE-", {"ok": True, "error": None})
    except Exception as e:
        window.write_event_value("-DOWNLOAD_DONE-", {"ok": False, "error": str(e)})


# --- GUI Layout ---
sg.theme("SystemDefault")

layout = [
    [sg.Text("Video URL:"), sg.InputText(key="-URL-", size=(50, 1))],
    [sg.Text("Save to:"),   sg.InputText(key="-FOLDER-", size=(40, 1)), sg.FolderBrowse()],
    [
        sg.Text("Type:"),
        sg.Combo(["Video", "Audio Only"], default_value="Video", key="-TYPE-", size=(15, 1), readonly=True, enable_events=True),
        sg.Text("Format:"),
        sg.Combo(["mp4", "mkv", "webm", "avi", "mov"], default_value="mp4", key="-VIDEO_FORMAT-", size=(15, 1), readonly=True),
        sg.Combo(["mp3", "m4a", "wav", "flac", "opus"], default_value="mp3", key="-AUDIO_FORMAT-", size=(15, 1), readonly=True, visible=False),
    ],
    [
        sg.Checkbox("Download single video only (no playlist)", default=True, key="-NO_PLAYLIST-"),
    ],
    [
        sg.Button("Download", key="-DOWNLOAD-"),
        sg.Button("Cancel",   key="-CANCEL-", disabled=True),
        sg.Button("Clear Log", key="-CLEAR-"),
        sg.Button("Exit"),
    ],
    [sg.Multiline(size=(70, 10), key="-LOG-", disabled=True, autoscroll=True)],
    [sg.Text("Progress: ", size=(15, 1)), sg.Text("", key="-PROGRESS_TEXT-", size=(50, 1))],
    [sg.ProgressBar(100, orientation='h', size=(59, 20), key='-PROGRESSBAR-')],
]

window = sg.Window("Media Downloader", layout, finalize=True)

downloading = False

# Event loop
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        # Gracefully stop the worker thread if it is running
        if downloading:
            cancel_flag = True
            window["-LOG-"].print("Waiting for download to cancel...")
            # Give the thread a moment to notice the flag
            if worker_thread and worker_thread.is_alive():
                worker_thread.join(timeout=2.0)
        break

    if event == "-DOWNLOAD-":
        url = values["-URL-"].strip()
        folder = values["-FOLDER-"] or os.getcwd()
        
        # Get type and format from dropdowns
        download_type = values["-TYPE-"]
        audio_only = (download_type == "Audio Only")
        
        if audio_only:
            output_format = values["-AUDIO_FORMAT-"]
        else:
            output_format = values["-VIDEO_FORMAT-"]
        
        no_playlist = values["-NO_PLAYLIST-"]

        if not url:
            sg.popup_error("No URL provided", "Please paste a video URL.")
            continue

        # Validate URL format
        if not url.startswith(("http://", "https://")):
            sg.popup_error("Invalid URL", "Please enter a URL starting with http:// or https://")
            continue

        if downloading:
            sg.popup_error("A download is already in progress.")
            continue

        # Check if folder is writable
        if not os.access(folder, os.W_OK):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                sg.popup_error("Folder Error", f"Cannot write to folder: {e}")
                continue

        window["-LOG-"].print(f"Starting download to: {folder}")
        window["-LOG-"].print(f"Type: {download_type} | Format: {output_format.upper()}")
        window["-LOG-"].print(f"Mode: {'Single video' if no_playlist else 'Playlist allowed'}")
        window["-LOG-"].print("-" * 70)

        downloading = True
        window["-DOWNLOAD-"].update(disabled=True)
        window["-CANCEL-"].update(disabled=False)
        window["-PROGRESSBAR-"].update(current_count=0)
        window["-PROGRESS_TEXT-"].update("")

        worker_thread = threading.Thread(
            target=start_download_in_thread,
            args=(url, folder, audio_only, output_format, no_playlist, window),
            daemon=False,  # Changed to False for better cleanup
        )
        worker_thread.start()

    elif event == "-TYPE-":
        # Show/hide appropriate format dropdown based on type
        if values["-TYPE-"] == "Audio Only":
            window["-VIDEO_FORMAT-"].update(visible=False)
            window["-AUDIO_FORMAT-"].update(visible=True)
        else:
            window["-VIDEO_FORMAT-"].update(visible=True)
            window["-AUDIO_FORMAT-"].update(visible=False)

    elif event == "-CANCEL-":
        if downloading:
            cancel_flag = True
            window["-LOG-"].print("Cancelling download...")
            window["-PROGRESS_TEXT-"].update("Cancelling...")

    elif event == "-CLEAR-":
        window["-LOG-"].update("")
        window["-PROGRESS_TEXT-"].update("")

    elif event == "-PROGRESS-":
        # Update progress display
        progress_data = values["-PROGRESS-"]
        
        if progress_data.get('status') == 'finished':
            window["-LOG-"].print(f"Finished downloading: {os.path.basename(progress_data.get('filename', ''))}")
        else:
            percent_str = progress_data.get('percent', 'N/A')
            speed = progress_data.get('speed', 'N/A')
            eta = progress_data.get('eta', 'N/A')
            
            progress_text = f"{percent_str} | Speed: {speed} | ETA: {eta}"
            window["-PROGRESS_TEXT-"].update(progress_text)
            
            # Try to extract numeric percentage for progress bar
            try:
                # Remove '%' and convert to float
                percent_num = float(percent_str.replace('%', '').strip())
                window["-PROGRESSBAR-"].update(current_count=int(percent_num))
            except (ValueError, AttributeError):
                pass

    elif event == "-DOWNLOAD_DONE-":
        # Worker thread signaled completion or error
        downloading = False
        window["-DOWNLOAD-"].update(disabled=False)
        window["-CANCEL-"].update(disabled=True)

        result = values["-DOWNLOAD_DONE-"]
        if result["ok"]:
            window["-LOG-"].print("=" * 70)
            window["-LOG-"].print("✓ Download completed successfully!")
            window["-LOG-"].print("=" * 70)
            window["-PROGRESS_TEXT-"].update("Complete!")
            sg.popup("Download Complete", "Your download finished successfully!", keep_on_top=True)
        else:
            error_msg = result["error"]
            window["-LOG-"].print("=" * 70)
            window["-LOG-"].print(f"✗ Error: {error_msg}")
            window["-LOG-"].print("=" * 70)
            window["-PROGRESS_TEXT-"].update("Failed")
            
            # Show more user-friendly error messages
            if "cancelled" in error_msg.lower():
                sg.popup("Cancelled", "Download was cancelled by user.", keep_on_top=True)
            else:
                sg.popup_error("Download Failed", error_msg, keep_on_top=True)

window.close()