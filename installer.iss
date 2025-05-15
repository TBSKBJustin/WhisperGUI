; ========= Whisper GUI (source‑mode) installer =========

[Setup]
AppName=Whisper GUI
AppVersion=0.1
DefaultDirName={pf}\Whisper GUI
DefaultGroupName=Whisper GUI
ArchitecturesInstallIn64BitMode=x64
ShowLanguageDialog=yes
OutputDir=.
OutputBaseFilename=WhisperGUI_Installer
DisableDirPage=no

[Languages]
Name: "en";  MessagesFile: "compiler:Default.isl"
Name: "chs"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Files]
; 复制启动器 exe
Source: "dist\WhisperGUI.exe"; DestDir: "{app}"; Flags: ignoreversion
; 复制源码
Source: "src\*"; DestDir: "{app}\src"; Flags: recursesubdirs createallsubdirs ignoreversion
; 复制图标
Source: "resources\icon.ico"; DestDir: "{app}\resources"; Flags: ignoreversion

[Icons]
Name: "{group}\Whisper GUI";      Filename: "{app}\WhisperGUI.exe"; IconFilename: "{app}\resources\icon.ico"
Name: "{userdesktop}\Whisper GUI"; Filename: "{app}\WhisperGUI.exe"; \
      IconFilename: "{app}\resources\icon.ico"; Tasks: desktopicon
      
[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon";  GroupDescription: "Additional icons:"; Flags: unchecked

[Code]
var
  PyPage: TInputOptionWizardPage;
  IsCN: Boolean;

procedure InitializeWizard();
begin
  IsCN := (ActiveLanguage = 'chs');

  { --- PyTorch 版本选择页 --- }
  if IsCN then
    PyPage := CreateInputOptionPage(
      wpWelcome, '选择 PyTorch 版本', '请选择要安装的 PyTorch 版本',
      'CPU‑only 版本体积较小；GPU 版本需下载更大文件', True, False)
  else
    PyPage := CreateInputOptionPage(
      wpWelcome, 'Select PyTorch Version', 'Choose the PyTorch build you want',
      'CPU‑only build is smaller; GPU build needs ~1.5 GB download', True, False);

  if IsCN then begin
    PyPage.Add('CPU‑only（≈200 MB）');
    PyPage.Add('GPU 版（CUDA，≈1.5 GB）');
  end else begin
    PyPage.Add('CPU‑only (≈200 MB)');
    PyPage.Add('GPU‑enabled (CUDA, ≈1.5 GB)');
  end;

  PyPage.Values[0] := True;
end;

function ExtraIndex(Param: String): String;
begin
  if PyPage.Values[1] then
    Result := ' --index-url https://download.pytorch.org/whl/cu118'
  else
    Result := '';
end;

[Run]
; ① 创建 venv（保持不变）
Filename: "{cmd}"; Parameters: "/C py -3 -m venv ""{app}\venv"""; Flags: runhidden waituntilterminated

; ② 安装 PyTorch  (CPU / GPU)
Filename: "{cmd}"; Parameters: "/C ""{app}\venv\Scripts\python.exe"" -m pip install torch torchvision torchaudio{code:ExtraIndex} --extra-index-url https://pypi.org/simple ffmpeg-python git+https://github.com/openai/whisper.git"; Flags: waituntilterminated

; ④ 启动程序
Filename: "{app}\WhisperGUI.exe"; Description: "{cm:LaunchProgram,Whisper GUI}"; Flags: nowait postinstall skipifsilent
