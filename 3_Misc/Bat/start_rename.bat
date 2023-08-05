@echo off
setlocal enabledelayedexpansion
dir /b/od
pause > nul
:: 将当前目录下的rename_by_time.bat文件复制到当前路径下所有文件夹内\
for /f "delims=" %%i in ('dir /b/od *.*') do (
    if not "%%i" =="%~nx0" (
        copy .\rename_by_time.bat %%i\
    )
)

pause > nul
:: 启动当前路径下所有文件夹内的rename_by_time.bat文件
for /f "delims=" %%i in ('dir /b/od *.*') do (
    if not "%%i" =="%~nx0" (
        %%i\rename_by_time.bat
    )
)
pause > nul