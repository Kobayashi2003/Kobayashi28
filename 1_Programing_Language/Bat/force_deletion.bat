@setlocal enableDelayedExpansion
@echo off
@REM echo the file or folder is being deleted
@REM echo %1

@REM check if the file or folder exists
if "%1"=="" (
    echo please drag and drop the file or folder you want to delete...
    pause >nul
    goto exit
)

@REM confirm deletion
echo Are you sure you want to delete %1?
echo be careful, this action is irreversible, your file or folder name better not contain '^&'
set /p delete= [y/n]
if %delete%==y goto delete

@REM exit if not confirmed
if %delete%==n goto exit

:delete
DEL /F /A /Q \\?\%1
RD /S /Q \\?\%1

:exit
exit