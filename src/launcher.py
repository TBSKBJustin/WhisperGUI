# launcher.py  (no console, keeps log handling)

import os, sys, subprocess, ctypes, webbrowser

base = os.path.dirname(os.path.abspath(sys.argv[0]))
py   = os.path.join(base, 'venv', 'Scripts', 'pythonw.exe')
main = os.path.join(base, 'src', 'main.py')
log  = os.path.join(base, 'runtime_log.txt')

def alert(msg):
    ctypes.windll.user32.MessageBoxW(0, msg, "Whisper GUI", 0x10)

for path, name in [(py, "Python runtime"), (main, "main.py")]:
    if not os.path.exists(path):
        alert(f"{name} not found:\n{path}")
        sys.exit(1)

# CREATE_NO_WINDOW keeps task‑bar icon = your EXE icon
flags = subprocess.CREATE_NO_WINDOW

proc = subprocess.Popen([py, main], cwd=base, creationflags=flags)
ret  = proc.wait()

if ret != 0:
    if os.path.exists(log):
        webbrowser.open(log)
    alert(f"Program exited with code {ret}.")
