@REM remove all files in Temp folder
@echo off
setlocal enabledelayedexpansion

set path="%~dp0Temp\"
set files=%path%*

for %%f in (%files%) do (
    del "%%f"
)