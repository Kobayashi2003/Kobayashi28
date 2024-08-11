@echo off

REM Powershell 5/6
powershell -NoProfile -File %~dp0\lfrc-preview.ps1 %0 %1 %2 %3 %4 %5 %6 %7 %8

REM Powershell 7+
REM pwsh -NoProfile -File %~dp0\lfrc-preview.ps1 %0 %1 %2 %3 %4 %5 %6 %7 %8