# Whisper GUI

**Whisper GUI** is a lightweight desktop application for transcribing audio and video files using OpenAI's Whisper model — no command-line knowledge required.

- 🎧 Supports MP4, MP3, WAV, FLAC, M4A, and more
- 🌍 Multilingual: Choose transcription language + subtitle format (TXT/SRT/VTT)
- 🧠 Model selection (tiny → large) for speed vs. accuracy
- ⚡ GPU or CPU selectable during installation
- 📦 Lightweight installer (under 30MB) downloads only what you need

---

## 💻 System Requirements

- Windows 10 or 11 (64-bit)
- Internet connection (for one-time dependency download)
- Python 3.10 – 3.13 (Python 3.13 embedded via virtual environment)
- [Optional] NVIDIA GPU with CUDA 11.8+ for GPU acceleration

---

## 🚀 Installation

1. **Download** the latest `WhisperGUI_Installer.exe` from [Releases](https://github.com/TBSKBJustin/WhisperGUI/releases)
2. Run the installer:
   - Select UI language (English / 简体中文)
   - Choose installation directory
   - Choose **PyTorch version**:
     - `CPU-only` (≈200MB download)
     - `GPU-enabled (CUDA)` (≈1.5GB download; requires CUDA 11.8+)
3. Installer will:
   - Create a Python virtual environment
   - Download and install required packages (`torch`, `whisper`, `ffmpeg-python`, etc.)
4. Upon completion, launch the app from:
   - Desktop shortcut
   - Start menu
   - Or run `{InstallDir}\WhisperGUI.exe`

---

## 🧠 How It Works

This GUI wraps the [OpenAI Whisper](https://github.com/openai/whisper) speech recognition model in a user-friendly interface.

- Under the hood:
  - Built with **Tkinter**
  - Whisper runs through a **dedicated Python venv**
  - Transcription output is saved to `.txt`, `.srt`, or `.vtt` formats
- No external tools needed (FFmpeg is handled via `ffmpeg-python`)

---

## 🗂 File Structure (Post-install)

Whisper GUI/
├─ WhisperGUI.exe ← Lightweight launcher (~7MB)
├─ venv/ ← Python virtual environment
├─ src/ ← Full Python source code
│ ├─ main.py
│ ├─ ui.py
│ ├─ transcriber.py
│ └─ translations.py
├─ resources/
│ └─ icon.ico
└─ install_log.txt ← Install output log (in case of issues)


---

## ❓ FAQ

### “I get an error saying `torch` or `whisper` not found after install.”
- This likely means the install process failed.
- Please check `install_log.txt` in the installation folder.
- Ensure you have internet access during install.
- For GPU users: make sure you have CUDA 11.8 drivers installed.

### Can I run this on a machine without Python?
- Yes! The app auto-creates its own Python environment inside the install folder.
- You do not need Python pre-installed.

### Can I upgrade Whisper or PyTorch later?
- Yes, open a terminal inside `{InstallDir}\venv\Scripts\` and run:


---

## 🛠 Developer Info

- Language: Python 3.13
- GUI: Tkinter
- Installer: [Inno Setup](https://jrsoftware.org/isinfo.php)
- Launcher compiled with [PyInstaller](https://pyinstaller.org/)

---

## 📄 License

MIT License © 2024 Justin

---

## 🌟 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [Inno Setup](https://jrsoftware.org/)

