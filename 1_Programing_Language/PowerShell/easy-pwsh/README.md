```
 __   __   __                                                        _           __   __   __
 \ \  \ \  \ \      ___   __ _  ___  _   _     _ __  __      __ ___ | |__       / /  / /  / /
  \ \  \ \  \ \    / _ \ / _` |/ __|| | | |   | '_ \ \ \ /\ / // __|| '_ \     / /  / /  / /
  / /  / /  / /   |  __/| (_| |\__ \| |_| |   | |_) | \ V  V / \__ \| | | |    \ \  \ \  \ \
 /_/  /_/  /_/     \___| \__,_||___/ \__, |   | .__/   \_/\_/  |___/|_| |_|     \_\  \_\  \_\
                                     |___/    |_|
```

```
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