# Whisper GUI

## 下载

前往 [Releases](https://github.com/yourname/whisper-gui/releases) 下载最新的 `WhisperGUI.exe`。

## 使用

1. 双击 `WhisperGUI.exe`。  
2. 选择源文件（支持 mp4/mp3/wav/... 等 FFmpeg 支持的格式）。  
3. 选择语言、模型、导出格式和目标文件夹。  
4. 点击 **Start**，等待转录完成。

## 自行打包（可选）

如果你想自己修改源码并打包：

```bash
git clone https://github.com/yourname/whisper-gui.git
cd whisper-gui
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name WhisperGUI main.py
