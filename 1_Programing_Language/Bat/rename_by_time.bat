@echo off
setlocal enabledelayedexpansion

:: clear screen
cls

:: show menu
echo    ~===================================================================
echo  @   -------------  welcome to the rename program  ------------------   @
echo  @  *    **    ****       ****         *         ****    *     *   **** @
echo  @  *  **    **    **    *    *       * *      *         *     *    **  @
echo  @  * **    **      **   *   **      *   *     *         *     *    **  @
echo  @  *       **      **   * ****     *     *     *****    *******    **  @
echo  @  * **    **      **   *      *  *********         *   *     *    **  @
echo  @  *   **   **    **    *     *  *         *        *   *     *    **  #
echo  @  *    **    ****       ****   *           *  ****     *     *   **** @
echo    ====================================================================
echo.
echo         [1] rename all files in current directory
echo         [2] rename all files in current directory and subdirectories
echo.
echo         Tips:if you don't want to rename some files, you can set their attributes to hidden
echo.

:: read user input
set /p choice=please input your choice:
    
:: output all files in current directory and subdirectories
::dir %~dp0 /b/od /s
::echo press enter to continue...
::pause > nul

:: create a new file named rename_sub.bat in current directory, 
::this file will be used to rename all files in the directory where it is located
:: -- rename_sub.bat start --
echo @echo off > rename_sub.bat
echo setlocal enabledelayedexpansion >> rename_sub.bat
echo set /a count=0 >> rename_sub.bat
echo for /f "delims=" %%%%i in ('dir %%~dp0 /b/od') do ( >> rename_sub.bat
echo     if not "%%%%i" == "rename_by_time.bat" ( >> rename_sub.bat
echo         if not "%%%%i" == "%%~nx0" ( >> rename_sub.bat
echo             if not "%%%%i" == "^!count^!%%%%~xi" ( >> rename_sub.bat
echo                 ren "%%~dp0\%%%%i" "^!count^!%%%%~xi" >> rename_sub.bat
echo             ) >> rename_sub.bat
echo         ) >> rename_sub.bat
echo         set /a count+=1 >> rename_sub.bat
echo     ) >> rename_sub.bat
echo ) >> rename_sub.bat
:: -- rename_sub.bat end --

:: if user input is 1, then rename all files in current directory
if "%choice%"=="1" (
    :: show all files in current directory
    dir %~dp0 /b/od
    echo press enter to continue...
    pause > nul
    :: then start rename_sub.bat to rename all files in current directory
    rename_sub.bat
    :: finally delete rename_sub.bat
    del rename_sub.bat
)

:: if user input is 2, then rename all files in current directory and subdirectories
if "%choice%"=="2" (
    :: show all files in current directory and subdirectories
    dir %~dp0 /b/od /s
    echo press enter to continue...
    pause > nul
    :: then copy the rename_sub.bat to all subdirectories 
    for /f "delims=" %%i in ('dir %~dp0 /b/od /ad /s') do (
        if exist "%%i"\rename_sub.bat del "%%i"\rename_sub.bat
        copy rename_sub.bat "%%i"
        echo successfully copy rename_sub.bat to %%i
        @REM pause > nul
    )
    :: then start rename_sub.bat to rename all files in current directory and subdirectories
    :: we need to start the rename_sub.bat from the deepest subdirectory to the current directory, if not, some problems will occur
    :: It is recubled from shallow to deep, so we need to reverse it to get the order we want
    dir %~dp0 /b/od /s /ad | sort /r > rename_temp.txt
    for /f "delims=" %%i in (rename_temp.txt) do (
        @REM echo %%i
        "%%i"\rename_sub.bat
        @REM pause > nul
    )
    :: finally delete rename_sub.bat and rename_temp.txt
    for /f "delims=" %%i in ('dir %~dp0 /b/od /ad /s') do (
        del "%%i"\rename_sub.bat
    )
    del rename_sub.bat
    del rename_temp.txt
)

:: if user input is not 1 or 2, then show error message
if not "%choice%"=="1" if not "%choice%"=="2" (
    echo invalid input, please input 1 or 2
    del rename_sub.bat
    echo press enter to continue...
    pause > nul
)