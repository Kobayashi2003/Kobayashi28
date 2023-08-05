@echo off
setlocal enabledelayedexpansion
echo "rename_by_time.bat is running..."
dir %~dp0 /b/od
set /a count=0
pause > nul
for /f "delims=" %%i in ('dir %~dp0 /b/od') do (
	if not "%%i" =="%~nx0" (
		set /a count+=1
		:: 将文件加下的文件按时间顺序重命名
		ren "%~dp0\%%i" "!count!%%~xi"
	)
)
pause > nul


