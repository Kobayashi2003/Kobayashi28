Add-Type -TypeDefinition @'
    using System;
    using System.Runtime.InteropServices;

    public struct RECT{
        public uint left;
        public uint top;
        public uint right;
        public uint bottom;
    }

    public struct POINT {
        public int X;
        public int Y;
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

        [DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)]
        public static extern short GetAsyncKeyState(int vkey);
    }

    public static class KeyboardSimulator {
        [DllImport("user32.dll")]
        private static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);

        [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true, CallingConvention = CallingConvention.Winapi)]
        public static extern short GetKeyState(int keyCode);

        private const int KEYEVENTF_EXTENDEDKEY = 0x1;
        private const int KEYEVENTF_KEYUP = 0x2;
        public const byte VK_CAPITAL = 0x14;
        public const byte VK_NUMLOCK = 0x90;
        public const byte VK_INSERT = 0x2D;

        public static void ToggleKey(byte keyCode)
        {
            keybd_event(keyCode, 0x45, KEYEVENTF_EXTENDEDKEY, UIntPtr.Zero);
            keybd_event(keyCode, 0x45, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, UIntPtr.Zero);
        }

        public static bool IsKeyToggled(byte keyCode)
        {
            return (((ushort)GetKeyState(keyCode)) & 0xffff) != 0;
        }
    }

    public static class MouseSimulator {
        [DllImport("user32.dll")]
        public static extern bool GetCursorPos(out POINT lpPoint);

        [DllImport("user32.dll")]
        public static extern bool SetCursorPos(int X, int Y);

        [DllImport("user32.dll")]
        public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

        public const int MOUSEEVENTF_LEFTDOWN = 0x0002;
        public const int MOUSEEVENTF_LEFTUP = 0x0004;
        public const int MOUSEEVENTF_RIGHTDOWN = 0x0008;
        public const int MOUSEEVENTF_RIGHTUP = 0x0010;
        public const int MOUSEEVENTF_MIDDLEDOWN = 0x0020;
        public const int MOUSEEVENTF_MIDDLEUP = 0x0040;
        public const int MOUSEEVENTF_WHEEL = 0x0800;

        public static POINT GetMousePosition()
        {
            POINT point;
            GetCursorPos(out point);
            return point;
        }

        public static void SetMousePosition(int x, int y)
        {
            SetCursorPos(x, y);
        }

        public static void MouseClick(int button)
        {
            POINT position = GetMousePosition();
            switch (button)
            {
                case 0: // Left click
                    mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, (uint)position.X, (uint)position.Y, 0, UIntPtr.Zero);
                    break;
                case 1: // Middle click
                    mouse_event(MOUSEEVENTF_MIDDLEDOWN | MOUSEEVENTF_MIDDLEUP, (uint)position.X, (uint)position.Y, 0, UIntPtr.Zero);
                    break;
                case 2: // Right click
                    mouse_event(MOUSEEVENTF_RIGHTDOWN | MOUSEEVENTF_RIGHTUP, (uint)position.X, (uint)position.Y, 0, UIntPtr.Zero);
                    break;
            }
        }

        public static void MouseDrag(int button, int startX, int startY, int endX, int endY, int steps)
        {
            // Move to start position
            SetCursorPos(startX, startY);

            // Press the mouse button
            switch (button)
            {
                case 0: // Left
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, UIntPtr.Zero);
                    break;
                case 1: // Middle
                    mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, UIntPtr.Zero);
                    break;
                case 2: // Right
                    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, UIntPtr.Zero);
                    break;
            }

            // Calculate step size
            int stepX = (endX - startX) / steps;
            int stepY = (endY - startY) / steps;

            // Move in steps
            for (int i = 0; i < steps; i++)
            {
                int currentX = startX + stepX * i;
                int currentY = startY + stepY * i;
                SetCursorPos(currentX, currentY);
                System.Threading.Thread.Sleep(10); // Small delay for smoother movement
            }

            // Ensure we reach the exact end position
            SetCursorPos(endX, endY);

            // Release the mouse button
            switch (button)
            {
                case 0: // Left
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, UIntPtr.Zero);
                    break;
                case 1: // Middle
                    mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, UIntPtr.Zero);
                    break;
                case 2: // Right
                    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, UIntPtr.Zero);
                    break;
            }
        }

        public static void ScrollWheel(int amount)
        {
            mouse_event(MOUSEEVENTF_WHEEL, 0, 0, (uint)amount, UIntPtr.Zero);
        }
    }
'@
