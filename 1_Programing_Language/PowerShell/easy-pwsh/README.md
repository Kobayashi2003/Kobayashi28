```
 _______    ________   ________        ___    ___     
|\  ___ \  |\   __  \ |\   ____\      |\  \  /  /|    
\ \   __/| \ \  \|\  \\ \  \___|_     \ \  \/  / /    
 \ \  \_|/__\ \   __  \\ \_____  \     \ \    / /     
  \ \  \_|\ \\ \  \ \  \\|____|\  \     \/  /  /      
   \ \_______\\ \__\ \__\ ____\_\  \  __/  / /        
    \|_______| \|__|\|__||\_________\|\___/ /         
                         \|_________|\|___|/          
 ________   ___       __    ________   ___  ___       
|\   __  \ |\  \     |\  \ |\   ____\ |\  \|\  \      
\ \  \|\  \\ \  \    \ \  \\ \  \___|_\ \  \\\  \     
 \ \   ____\\ \  \  __\ \  \\ \_____  \\ \   __  \    
  \ \  \___| \ \  \|\__\_\  \\|____|\  \\ \  \ \  \   
   \ \__\     \ \____________\ ____\_\  \\ \__\ \__\  
    \|__|      \|____________||\_________\\|__|\|__|  
                              \|_________|            

                                       

                                       _            _                                _      _
                                      | | __  ___  | |__    __ _  _   _   __ _  ___ | |__  (_)
                         _____        | |/ / / _ \ | '_ \  / _` || | | | / _` |/ __|| '_ \ | |
                        |_____|       |   < | (_) || |_) || (_| || |_| || (_| |\__ \| | | || |
                                      |_|\_\ \___/ |_.__/  \__,_| \__, | \__,_||___/|_| |_||_|
                                                                  |___/
```

# Usage

- before you start, you should set your ExecutionPolicy to `RemoteSigned` or `AllSigned`:

```powershell
set-executionpolicy -scope currentuser -executionpolicy remotesigned
# or
set-executionpolicy -scope currentuser -executionpolicy allsigned
``` 

- than download easy-pwsh to your local directory, and run it:

```powershell
> cd easy-pwsh
> ./easy-pwsh.ps1 -i
```