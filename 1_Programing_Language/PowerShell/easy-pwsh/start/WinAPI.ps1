Add-Type -TypeDefinition @'
    using System;
    using System.Runtime.InteropServices;

    public struct RECT{
        public uint left;
        public uint top;
        public uint right;
        public uint bottom;
    }

    public static class WinApi {
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
        [DllImport("user32.dll", SetLastError=true)]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError=true)]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll", SetLastError=true)]
        public static extern bool IsIconic(IntPtr hWnd);    // Is the window minimized?
    }
'@
