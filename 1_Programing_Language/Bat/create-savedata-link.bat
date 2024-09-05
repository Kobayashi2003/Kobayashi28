@echo off
setlocal enabledelayedexpansion

pushd %~dp0 & cd /d %~dp0
%1 mshta vbscript:createobject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&goto :EOF
:runas

set item_path=HENTAI LABYRINTH
set link_path=D:\Documents\AliceSoft\

if not exist "%link_path%" mkdir "%link_path%"

if not exist "%item_path%" (
    echo %item_path% not found!
) else if exist "%link_path%\%item_path%" (
    echo %item_path% already exist!
) else (
    cmd /c "powershell -NoProfile -Command New-Item -ItemType SymbolicLink -Path '%link_path%\%item_path%' -Target '%item_path%'"
    echo Done! Link created at %link_path%\%item_path%.
)

echo Press any key to exit...
pause >nul
exit