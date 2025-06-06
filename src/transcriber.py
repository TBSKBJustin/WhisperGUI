import os, sys, subprocess, json, re
from translations import UI_TEXT

# Match lines like "[00:04.080 --> 00:06.400]" emitted by Whisper CLI
ARROW_RE = re.compile(r"\[(\d+):(\d+\.\d+)\s+-->\s+(\d+):(\d+\.\d+)]")
# Fallback for tqdm output lines showing percentage
TQDM_RE = re.compile(r"(\d+)%\|")

def _probe_duration(path: str) -> float:
    """Return audio length in seconds using ffprobe if available."""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=duration", "-of", "json", path
        ], text=True, stderr=subprocess.DEVNULL)
        data = json.loads(out)
        return float(data['streams'][0]['duration'])
    except Exception:
        return 0.0

def format_srt_time(t): 
    h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_vtt_time(t):
    h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def transcribe(src, out_dir, lang, model_size, export_type, ui_lang, progress_callback):
    """Transcribe by running the Whisper CLI so progress can be parsed."""
    texts = UI_TEXT[ui_lang]

    if not os.path.isfile(src):
        return {'error': texts.get('err_no_file', 'Invalid source file')}
    if not os.path.isdir(out_dir):
        return {'error': texts.get('err_no_out', 'Invalid output folder')}

    total_sec = _probe_duration(src)
    cmd = [
        sys.executable, '-u', '-m', 'whisper', src,
        '--model', model_size,
        '--output_format', export_type,
        '--output_dir', out_dir
    ]
    if lang.lower() != 'auto':
        cmd += ['--language', lang]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )

    for raw in iter(proc.stdout.readline, ''):
        print(raw, end='')

        m = ARROW_RE.search(raw)
        if m and total_sec:
            cur = int(m.group(1)) * 60 + float(m.group(2))
            pct = int(min(cur / total_sec, 1) * 100)
            progress_callback(pct)
            continue

        n = TQDM_RE.search(raw)
        if n:
            pct = int(n.group(1))
            progress_callback(pct)

    ret = proc.wait()
    if ret != 0:
        print(f"\n❌ Error {ret}\n")
        return {'error': f'whisper exited with code {ret}'}

    progress_callback(100)
    base = os.path.splitext(os.path.basename(src))[0]
    out_path = os.path.join(out_dir, f'{base}.{export_type}')
    print("\n✅ Done\n")
    return {'path': out_path}
