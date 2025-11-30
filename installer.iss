; ----------------------------------------------------------
; MySQL Learner Installer (Inno Setup 6)
; Clean, Updated Version — No Assets Folder
; ----------------------------------------------------------

[Setup]
AppName=MySQL Learner
AppVersion=1.0
AppPublisher=Your Company
DefaultDirName={pf}\MySQL Learner
DefaultGroupName=MySQL Learner
OutputDir=.
OutputBaseFilename=MySQL_Learner_Installer
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
ArchitecturesInstallIn64BitMode=x64

; Optional: If you want to set an icon for the installer, uncomment:
; SetupIconFile=..\icon.ico

[Files]
; --------------------------
; Main EXE from PyInstaller
; --------------------------
Source: "..\dist\MySQL_Learner.exe"; DestDir: "{app}"; Flags: ignoreversion

; --------------------------
; Lessons Folder
; --------------------------
Source: "..\lessons\*"; DestDir: "{app}\lessons"; Flags: ignoreversion recursesubdirs createallsubdirs

; --------------------------
; Quizzes Folder
; --------------------------
Source: "..\quizzes\*"; DestDir: "{app}\quizzes"; Flags: ignoreversion recursesubdirs createallsubdirs

; --------------------------
; Practice Problems
; --------------------------
Source: "..\practice\*"; DestDir: "{app}\practice"; Flags: ignoreversion recursesubdirs createallsubdirs

; --------------------------
; Case Study Folder
; --------------------------
Source: "..\case_study\*"; DestDir: "{app}\case_study"; Flags: ignoreversion recursesubdirs createallsubdirs

; --------------------------
; SQLite Database Folder
; --------------------------
Source: "..\database\*"; DestDir: "{app}\database"; Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
; Start Menu shortcut
Name: "{group}\MySQL Learner"; Filename: "{app}\MySQL_Learner.exe"

; Optional desktop shortcut
Name: "{commondesktop}\MySQL Learner"; Filename: "{app}\MySQL_Learner.exe"; Tasks: desktopicon


[Tasks]
; Checkbox in installer for desktop shortcut
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked


[Run]
; Run app automatically after installation
Filename: "{app}\MySQL_Learner.exe"; Description: "Launch MySQL Learner"; Flags: nowait postinstall
