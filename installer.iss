

[Setup]
AppName=Whisper GUI
AppVersion=0.0.2
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

Source: "dist\WhisperGUI.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "src\*"; DestDir: "{app}\src"; Flags: recursesubdirs createallsubdirs ignoreversion

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


  if IsCN then
    PyPage := CreateInputOptionPage(
      wpWelcome, '选择 PyTorch 版本', '请选择要安装的 PyTorch 版本',
      'CPU‑only 版本体积较小；GPU 版本需下载更大文件', True, False)
  else
    PyPage := CreateInputOptionPage(
      wpWelcome, 'Select PyTorch Version', 'Choose the PyTorch build you want',
      'CPU‑only build is smaller; GPU build needs ~6 GB download', True, False);

  if IsCN then begin
    PyPage.Add('CPU‑only（≈1.5 GB）');
    PyPage.Add('GPU 版（CUDA，≈6 GB）');
  end else begin
    PyPage.Add('CPU‑only (≈1.5 GB)');
    PyPage.Add('GPU‑enabled (CUDA, ≈6 GB)');
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

Filename: "{cmd}"; Parameters: "/C py -3 -m venv ""{app}\venv"""; Flags: runhidden waituntilterminated


Filename: "{cmd}"; Parameters: "/C ""{app}\venv\Scripts\python.exe"" -m pip install torch torchvision torchaudio{code:ExtraIndex} --extra-index-url https://pypi.org/simple ffmpeg-python git+https://github.com/openai/whisper.git"; Flags: waituntilterminated


Filename: "{app}\WhisperGUI.exe"; Description: "{cm:LaunchProgram,Whisper GUI}"; Flags: nowait postinstall skipifsilent
