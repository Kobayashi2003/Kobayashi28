function pkill($name) {
    Get-Process $name -ErrorAction SilentlyContinue | Stop-Process
}