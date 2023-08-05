@REM remove all the exe files in Debug folder and the o files in Debug/InLinux folder

@echo off
setlocal enabledelayedexpansion

set "path=%~dp0Debug\"
set "files=%path%*.exe"

for %%f in (%files%) do (
    del "%%f"
)

set "path=%~dp0Debug\InLinux\"
set "files=%path%*.o"

for %%f in (%files%) do (
    del "%%f"
)