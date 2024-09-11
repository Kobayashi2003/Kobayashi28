@echo off
powershell.exe -NoProfile -Command 	"Clear-RecycleBin -Confirm:$false *>$null"
