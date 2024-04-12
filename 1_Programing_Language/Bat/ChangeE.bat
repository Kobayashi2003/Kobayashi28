@echo off
setlocal enabledelayedexpansion

@REM input 
echo choose the explorer version:
echo 1 : win10
echo 2 : win11
echo input the number: [1/2]
set /p mode=
if %mode%==1 goto win10E
if %mode%==2 goto win11E
goto exit

@REM win10 explorer
:win10E:
reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
goto exit

@REM win11 explorer
:win11E:
reg delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /va /f
goto exit

:exit
exit
