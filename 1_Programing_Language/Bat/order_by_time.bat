@echo off
setlocal enabledelayedexpansion

cmd /c Powershell -NoProfile -Command "(( & D:\Program\anaconda3\Scripts\conda.exe 'shell.powershell' 'hook') | Out-String | Invoke-Expression) ; (python D:\Program\Code\1_Programing_Language\Python\Practice\Prac_121To200\prc_122_group_by_time\group_by_time.py C:\Users\KOBAYASHI\Desktop\T --month -cs)"