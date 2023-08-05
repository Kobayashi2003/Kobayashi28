$Directory = "C:\Users\17312\Desktop\open"
Get-ChildItem $Directory | Rename-Item -NewName { $_.name -Replace " ","_"}