import json, os, pathlib

CFG_DIR  = pathlib.Path(os.getenv("APPDATA", "~")).expanduser() / "WhisperGUI"
CFG_DIR.mkdir(exist_ok=True)
CFG_PATH = CFG_DIR / "settings.json"

DEFAULTS = {"ui_lang": "en"}

def load():
    if CFG_PATH.exists():
        try:
            with open(CFG_PATH, "r", encoding="utf-8") as f:
                return {**DEFAULTS, **json.load(f)}
        except Exception:
            pass
    return DEFAULTS.copy()

def save(cfg: dict):
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
