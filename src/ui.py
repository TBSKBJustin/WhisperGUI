import os, sys, ctypes, tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from translations import UI_TEXT
from transcriber import transcribe
from config import load as load_cfg, save as save_cfg


class WhisperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg = load_cfg()


        try:
            myappid = u"Whisper.GUI.v0.0.2"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass


        try:
            if getattr(sys, "frozen", False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            icon_path = os.path.join(base_path, "resources", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print("Icon load failed:", e)


        self.ui_lang = self.cfg.get("ui_lang", "en")
        self._build_ui()

    def _switch(self, lang):
        self.ui_lang = lang
        self.cfg["ui_lang"] = lang
        save_cfg(self.cfg)
        self._build_ui()   

    def _build_ui(self):
        self.texts = UI_TEXT[self.ui_lang]
        self.title("Whisper GUI")

        for w in self.winfo_children(): w.destroy()

        menubar = tk.Menu(self)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label=self.texts['menu_exit'], command=self.quit)
        menubar.add_cascade(label=self.texts['menu_file'], menu=filem)
        settingm = tk.Menu(menubar, tearoff=0)
        uim = tk.Menu(settingm, tearoff=0)
        uim.add_command(label=UI_TEXT['en']['menu_ui_en'], command=lambda: self._switch('en'))
        uim.add_command(label=UI_TEXT['zh']['menu_ui_zh'], command=lambda: self._switch('zh'))
        settingm.add_cascade(label=self.texts['menu_ui_lang'], menu=uim)
        menubar.add_cascade(label=self.texts['menu_setting'], menu=settingm)
        aboutm = tk.Menu(menubar, tearoff=0)
        aboutm.add_command(label=self.texts['about_title'], command=self._show_about)
        menubar.add_cascade(label=self.texts['menu_about'], menu=aboutm)
        self.config(menu=menubar)


        f = ttk.Frame(self, padding=10); f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text=self.texts['source_file']).grid(row=0, column=0, sticky='w')
        self.file_e = ttk.Entry(f, width=50); self.file_e.grid(row=0, column=1, sticky='ew')
        ttk.Button(f, text=self.texts['browse'], command=self._browse_file).grid(row=0, column=2)

        ttk.Label(f, text=self.texts['trans_lang']).grid(row=1, column=0, sticky='w')
        self.lang_c = ttk.Combobox(f, values=['en','zh','ja','fr','de','auto'], width=6); self.lang_c.set('auto')
        self.lang_c.grid(row=1, column=1, sticky='w')
        ttk.Label(f, text=self.texts['model']).grid(row=1, column=1, padx=(100,0), sticky='w')
        self.mod_c = ttk.Combobox(f, values=['tiny','base','small','medium','large'], width=7); self.mod_c.set('base')
        self.mod_c.grid(row=1, column=1, padx=(150,0), sticky='w')
        ttk.Label(f, text=self.texts['export_type']).grid(row=1, column=1, padx=(260,0), sticky='w')
        self.typ_c = ttk.Combobox(f, values=['txt','srt','vtt'], width=5); self.typ_c.set('srt')
        self.typ_c.grid(row=1, column=1, padx=(330,0), sticky='w')

        ttk.Label(f, text=self.texts['export_loc']).grid(row=2, column=0, sticky='w')
        self.out_e = ttk.Entry(f, width=50); self.out_e.grid(row=2, column=1, sticky='ew')
        ttk.Button(f, text=self.texts['browse'], command=self._browse_folder).grid(row=2, column=2)

        self.start_b = ttk.Button(f, text=self.texts['start'], command=self._on_start)
        self.start_b.grid(row=3, column=1, sticky='w', pady=10)
        self.cancel_b = ttk.Button(f, text=self.texts['cancel'], command=self._on_cancel, state='disabled')
        self.cancel_b.grid(row=3, column=1, padx=(60,0), pady=10)

        self.prog = ttk.Progressbar(f, orient='horizontal', length=400, mode='determinate')
        self.prog.grid(row=4, column=0, columnspan=3, pady=(0,10))
        f.columnconfigure(1, weight=1)

    def _show_about(self):
        messagebox.showinfo(self.texts['about_title'],
                            f"{self.texts['about_title']}\nWhisper GUI v0.0.2\nAuthor: Justin")

    def _browse_file(self):
        p = filedialog.askopenfilename(
            filetypes=[
                ("All supported", "*.mp4 *.mp3 *.wav *.flac *.m4a *.aac *.ogg *.avi *.mkv *.webm"),
                ("Video files",   "*.mp4 *.mkv *.avi *.webm"),
                ("Audio files",   "*.mp3 *.wav *.flac *.m4a *.aac *.ogg")
            ]
        )
        if p: self.file_e.delete(0,tk.END); self.file_e.insert(0,p)

    def _browse_folder(self):
        p = filedialog.askdirectory()
        if p: self.out_e.delete(0,tk.END); self.out_e.insert(0,p)

    def _on_start(self):

        src     = self.file_e.get()
        out_dir = self.out_e.get() or os.path.dirname(src)
        lang    = self.lang_c.get()
        model   = self.mod_c.get()
        typ     = self.typ_c.get()
        ui_lang = self.ui_lang


        self.start_b.state(['disabled'])
        self.cancel_b.state(['!disabled'])
        self.prog['value'] = 0


        threading.Thread(
            target=self._run_transcribe,
            args=(src, out_dir, lang, model, typ, ui_lang, self._update_progress),
            daemon=True
        ).start()

    def _update_progress(self, v):
        self.prog['value'] = v

    def _run_transcribe(self, src, out_dir, lang, model, typ, ui_lang, prog_cb):
        res = transcribe(src, out_dir, lang, model, typ, ui_lang, prog_cb)
        if 'error' in res:
            messagebox.showerror("Error", res['error'])
        else:
            messagebox.showinfo("Done", f"Saved: {res['path']}")
        self.cancel_b.state(['disabled']); self.start_b.state(['!disabled'])

    def _on_cancel(self):

        messagebox.showinfo("Info", "Cannot cancel mid-task yet.")

