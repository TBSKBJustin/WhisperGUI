# transcriber.py
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
    # 验证输入/输出
    if not os.path.isfile(src):
        return {'error': texts.get('err_no_file', 'Invalid source file')}
    if not os.path.isdir(out_dir):
        return {'error': texts.get('err_no_out', 'Invalid output folder')}

    # Step 1: 加载模型
    progress_callback(5)
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        return {'error': f"Model load failed: {e}"}

    # Step 2: 转录
    progress_callback(20)
    try:
        result = model.transcribe(src, language=lang)
    except Exception as e:
        return {'error': f"Transcription failed: {e}"}

    # Step 3: 写文件
    progress_callback(60)
    base = os.path.splitext(os.path.basename(src))[0]
    out_path = os.path.join(out_dir, f"{base}.{export_type}")
    segments = result.get('segments', [])
    with open(out_path, 'w', encoding='utf-8') as f:
        if export_type == 'txt':
            f.write(result['text'])
        else:
            if export_type == 'vtt':
                f.write("WEBVTT\n\n")
            for i, seg in enumerate(segments, start=1):
                start, end, text = seg['start'], seg['end'], seg['text'].strip()
                if export_type == 'srt':
                    f.write(f"{i}\n")
                    f.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
                    f.write(text + "\n\n")
                else:  # vtt
                    f.write(f"{i}\n")
                    f.write(f"{format_vtt_time(start)} --> {format_vtt_time(end)}\n")
                    f.write(text + "\n\n")

    # Step 4: 完成
    progress_callback(100)
    return {'path': out_path}
