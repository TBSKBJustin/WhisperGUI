# launcher.py
import subprocess, os, sys, ctypes, webbrowser

base = os.path.dirname(os.path.abspath(sys.argv[0]))
py   = os.path.join(base, 'venv', 'Scripts', 'python.exe')
main = os.path.join(base, 'src', 'main.py')

def alert(msg):
    ctypes.windll.user32.MessageBoxW(0, msg, "Whisper GUI", 0x10)

if not os.path.exists(py):
    alert(f"Python runtime not found:\n{py}")
    sys.exit(1)
if not os.path.exists(main):
    alert(f"main.py missing:\n{main}")
    sys.exit(1)

proc = subprocess.Popen([py, main], cwd=base)
ret  = proc.wait()
if ret != 0:
    log = os.path.join(base, 'install_log.txt')
    if os.path.exists(log):
        webbrowser.open(log)
    alert("Program exited with code %d.\nPlease check install_log.txt" % ret)
