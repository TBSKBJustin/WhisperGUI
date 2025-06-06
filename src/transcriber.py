import os, whisper
from translations import UI_TEXT

def format_srt_time(t): 
    h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_vtt_time(t):
    h = int(t//3600); m = int((t%3600)//60); s = int(t%60); ms = int((t-int(t))*1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def transcribe(src, out_dir, lang, model_size, export_type, ui_lang, progress_callback):
    texts = UI_TEXT[ui_lang]

    if not os.path.isfile(src):
        return {'error': texts.get('err_no_file', 'Invalid source file')}
    if not os.path.isdir(out_dir):
        return {'error': texts.get('err_no_out', 'Invalid output folder')}


    progress_callback(5)
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        return {'error': f"Model load failed: {e}"}


    progress_callback(20)
    try:
        lang_arg = None if str(lang).lower() == 'auto' else lang

        def cb(p):
            try:
                pct = 20 + 60 * float(p)
                progress_callback(min(80, pct))
            except Exception:
                pass

        result = model.transcribe(src, language=lang_arg, progress_callback=cb)
    except Exception as e:
        return {'error': f"Transcription failed: {e}"}


    progress_callback(80)
    base = os.path.splitext(os.path.basename(src))[0]
    out_path = os.path.join(out_dir, f"{base}.{export_type}")
    segments = result.get('segments', [])
    with open(out_path, 'w', encoding='utf-8') as f:
        if export_type == 'txt':
            f.write(result['text'])
        else:
            if export_type == 'vtt':
                f.write("WEBVTT\n\n")
            total = max(len(segments), 1)
            for i, seg in enumerate(segments, start=1):
                start, end, text = seg['start'], seg['end'], seg['text'].strip()
                if export_type == 'srt':
                    f.write(f"{i}\n")
                    f.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
                    f.write(text + "\n\n")
                else:
                    f.write(f"{i}\n")
                    f.write(f"{format_vtt_time(start)} --> {format_vtt_time(end)}\n")
                    f.write(text + "\n\n")

                progress_callback(80 + 20 * (i / total))


    progress_callback(100)
    return {'path': out_path}
