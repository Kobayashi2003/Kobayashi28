cls
#Windows API
$code = @'
    using System.Runtime.InteropServices;
    public static class WinApi{
        [DllImport("user32.dll")]
        public static extern bool SetWindowPos(uint hWnd,uint hAfter,uint x,uint y,uint cx,uint cy,uint flags);
        [DllImport("kernel32.dll")]
        public static extern uint GetConsoleWindow();

		[DllImport("user32.dll")]
		public static extern bool ShowWindowAsync(uint hWnd, int nCmdShow);
    }
'@
Add-Type -TypeDefinition $code
#设置CMD窗口位置及大小
$hwnd = [WinApi]::GetConsoleWindow()
[void][WinApi]::SetWindowPos($hwnd, $null, 30, 30, 400, 500, 0)
#-------------------------------------------------------------------------
#启动记事本
Stop-Process -Name 'notepad' -Force -ErrorAction SilentlyContinue
Start-Process 'notepad'
Start-Sleep -Seconds 1
$hwnd = (Get-Process 'notepad')[0].MainWindowHandle
# 最小化窗口
[void][WinApi]::ShowWindowAsync([int]$hwnd, 2)
# 恢复窗口
[void][WinApi]::ShowWindowAsync([int]$hwnd, 4)
# 关闭记事本
#Stop-Process -Name Notepad