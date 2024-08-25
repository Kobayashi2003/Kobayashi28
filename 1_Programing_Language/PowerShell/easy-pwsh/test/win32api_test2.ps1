#&cls&@powershell -c "Get-Content '%~0' | Out-String | Invoke-Expression" &pause&exit

cls

#Windows API
$code=@'
    using System;
    using System.Runtime.InteropServices;
    public struct RECT{
        public uint left;
        public uint top;
        public uint right;
        public uint bottom;
    }
    public static class WinApi{
        [DllImport("user32.dll")]
        public static extern bool SetWindowPos(uint hWnd,uint hAfter,uint x,uint y,uint cx,uint cy,uint flags);
        [DllImport("kernel32.dll")]
        public static extern uint GetConsoleWindow();
        [DllImport("user32.dll")]
        public static extern bool GetWindowRect(uint hwnd, ref RECT rect);
        [DllImport("user32.dll")]
        public static extern uint GetDC(uint hwnd);
        [DllImport("gdi32.dll")]
        public static extern uint GetDeviceCaps(uint hdc, int index);

        public static uint[] GetScreen(){
            uint[] arr = {0,0};
            uint hdc = GetDC(0);
            arr[0] = GetDeviceCaps(hdc,118);
            arr[1] = GetDeviceCaps(hdc,117);
            return arr;
        }
    }
'@
Add-Type -TypeDefinition $code

#获取记事本窗口句柄
$hwnd = (Get-Process 'notepad')[0].MainWindowHandle
#获取窗口信息
$rect = New-Object 'RECT'
[void][WinApi]::GetWindowRect([int]$hwnd,[ref]$rect)
$screen = [WinApi]::GetScreen()
#计算水平居中坐标
$x = ($screen[0] - ($rect.right - $rect.left))/2
#设置记事本水平居中
[WinApi]::SetWindowPos([int]$hwnd,$null,$x,$rect.top,0,0,1)