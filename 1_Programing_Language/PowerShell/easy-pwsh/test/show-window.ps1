$sig = '[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);'
Add-Type -MemberDefinition $sig -name NativeMethods -namespace Win32

$SW_NORMAL = 1
$SW_MAXIMIZE = 3
$SW_MINIMIZE = 6

Stop-Process -Name notepad -ea 0
Start-Process notepad
Start-Sleep 2

$hWnd = (Get-Process notepad).MainWindowHandle

[Win32.NativeMethods]::ShowWindow($hWnd, $SW_MINIMIZE)
Start-Sleep 2

[Win32.NativeMethods]::ShowWindow($hWnd, $SW_MAXIMIZE)
Start-Sleep 2

[Win32.NativeMethods]::ShowWindow($hWnd, $SW_NORMAL)
Start-Sleep 2

Stop-Process -Name notepad -ea 0