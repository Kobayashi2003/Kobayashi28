@echo off
setlocal enabledelayedexpansion

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

@REM first check if the GetConsoleSize.exe & main.exe exists
if not exist GetConsoleSize.exe goto :EOF
if not exist main.exe goto :EOF

@REM start the GetConsoleSize.exe & main.exe, run the GetConsoleSize.exe and main.exe in the background
start /b GetConsoleSize.exe
start /b main.exe

@REM wait for the main.exe to finish, and if the main.exe stop, however the GetConsoleSize.exe still running, then kill the GetConsoleSize.exe
:wait
tasklist /fi "imagename eq main.exe" | find /i "main.exe" >nul
if errorlevel 1 goto :kill
timeout /t 1 /nobreak >nul
goto :wait

:kill
taskkill /f /im GetConsoleSize.exe >nul
