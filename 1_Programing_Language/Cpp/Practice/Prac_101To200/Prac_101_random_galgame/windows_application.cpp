// If you run this code by g++, you should add -mwindows to the command line.

/* [Walkthrough: Creating Windows Desktop Applications (C++)](https://learn.microsoft.com/en-us/previous-versions/bb384843(v=vs.140)) */
/* [Win32 和 C++ 入门](https://learn.microsoft.com/zh-cn/windows/win32/learnwin32/learn-to-program-for-windows) */

#include <windows.h>
#include <tchar.h>
#include <cstdlib>
#include <cstring>

/* what A, W, ExA, ExW means in Windows API?
     A: use ANSI character set
     W: use Unicode character set
     Ex: use extended version of the function
     ExA: the combination of Ex and A
     ExW: the combination of Ex and W
*/

static const TCHAR szWindowClass[] = _T("win32app");                // The main window class name.
static const TCHAR szTitle[] = _T("Win32 Guided Tour Application"); // The string that appears in the application's title bar.

HINSTANCE hInst;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {

    /* WinMain function : The application entry point.
    [in] HINSTANCE hInstance        : A handle to the current instance of the application.
    [in] HINSTANCE hPrevInstance    : Always NULL, obsolete.
    [in] LPSTR lpCmdLine            : The command line for the application, excluding the program name.
    [in] int nCmdShow                : Controls how the window is to be shown. This parameter can be one of the following values.
                                        SW_HIDE             : Hides the window and activates another window.
                                        SW_MAXIMIZE         : Maximizes the specified window.
                                        SW_MINIMIZE         : Minimizes the specified window and activates the next top-level window in the Z order.
                                        SW_RESTORE          : Activates and displays the window. If the window is minimized or maximized, Windows restores it to its original size and position.
                                        SW_SHOW             : Activates the window and displays it in its current size and position.
                                        SW_SHOWDEFAULT      : Sets the show state based on the SW_ value specified in the STARTUPINFO structure passed to the CreateProcess function by the program that started the application.
                                        SW_SHOWMAXIMIZED    : Activates the window and displays it as a maximized window.
                                        SW_SHOWMINIMIZED    : Activates the window and displays it as a minimized window.
                                        SW_SHOWMINNOACTIVE  : Displays the window as a minimized window. The active window remains active.
                                        SW_SHOWNA           : Displays the window in its current state. The active window remains active.
                                        SW_SHOWNOACTIVATE   : Displays a window in its most recent size and position. The active window remains active.
                                        SW_SHOWNORMAL       : Activates and displays a window. If the window is minimized or maximized, Windows restores it to its original size and position. An application should specify this flag when displaying the window for the first time.
    */

    WNDCLASSEX wcex;                                                    // The window class structure.
                                                                        // This structure contains information about the window such as its style, procedure, icon, cursor, background color, and so on.
    wcex.cbSize         = sizeof(WNDCLASSEX);                           // The size of the structure.
    wcex.style          = CS_HREDRAW | CS_VREDRAW;                      // The class style. CS_HREDRAW and CS_VREDRAW specify that when the window is resized horizontally or vertically, the entire window is repainted.
    wcex.lpfnWndProc    = WndProc;                                      // A pointer to the window procedure. WndProc function is use to handle messages sent to the window.
    wcex.cbClsExtra     = 0;                                            // The number of extra bytes to allocate following the window-class structure.
    wcex.cbWndExtra     = 0;                                            // The number of extra bytes to allocate following the window instance.
    wcex.hInstance      = hInstance;                                    // A handle to the instance that contains the window procedure for the class.
    wcex.hIcon          = LoadIcon(hInstance, IDI_APPLICATION);         // A handle to the class icon, which is displayed in the upper left corner of the window's client area.
    wcex.hCursor        = LoadCursor(NULL, IDC_ARROW);                  // A handle to the class cursor.
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW + 1);                   // A handle to the class background brush.
    wcex.lpszMenuName   = NULL;                                         // A pointer to a null-terminated string that specifies the resource name of the class menu, as the name appears in the resource file.
    wcex.lpszClassName  = szWindowClass;                                // A pointer to a null-terminated string or a class atom. This string or atom is the name of the window class.
    wcex.hIconSm        = LoadIcon(wcex.hInstance, IDI_APPLICATION);    // A handle to a small icon that is associated with the window class.

    /*
      [GetSockObject](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/nf-wingdi-getstockobject)
      [LoadIcon](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-loadicona)
      [LoadCursor](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-loadcursora)
    */

    // Register the window class.
    if (!RegisterClassEx(&wcex)) {
        MessageBox(NULL, _T("Call to RegisterClassEx failed!"), _T("Win32 Guided Tour"), NULL);
        return 1;
    }

    hInst = hInstance;

    HWND hWnd = CreateWindow(szWindowClass,         // The name of the window class.
                             szTitle,               // The window title.
                             WS_OVERLAPPEDWINDOW,   // The window style.
                             CW_USEDEFAULT,         // The x position of the window.
                             CW_USEDEFAULT,         // The y position of the window.
                             500,                   // The width of the window.
                             100,                   // The height of the window.
                             NULL,                  // A handle to the parent or owner window, depending on the window style.
                             NULL,                  // A handle to a menu, or specifies a child-window identifier depending on the window style.
                             hInstance,             // A handle to the instance of the module to be associated with the window.
                             NULL);                 // Pointer to a value to be passed to the window through the CREATESTRUCT structure passed in the lParam parameter of the WM_CREATE message.

    if (!hWnd) {
        MessageBox(NULL, _T("Call to CreateWindow failed!"), _T("Win32 Guided Tour"), NULL);
        return 1;
    }

    ShowWindow(hWnd, nCmdShow); // Show the window.
    UpdateWindow(hWnd);         // Update the window.
    

    // Main message loop.
    MSG msg;
    while (GetMessage(&msg, // [out] LPMSG lpMsg : A pointer to an MSG structure that receives message information from the message queue.
                      NULL, // [in]  HWND hWnd : A handle to the window whose messages are to be retrieved. The window must belong to the current thread.
                      0,    // [in]  UINT wMsgFilterMin : The integer value of the lowest message value to be retrieved.
                      0)    // [in]  UINT wMsgFilterMax : The integer value of the highest message value to be retrieved.
    ) { // If applications process virtual-key messages for some other purpose,
        // they should not call TranslateMessage.
        TranslateMessage(&msg); // [in] const MSG *lpMsg : A pointer to an MSG structure that contains message information.
        DispatchMessage(&msg);  // [in] const MSG *lpMsg : A pointer to an MSG structure that contains message information.
    }
    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {

    /* WndProc function : The window procedure is the function that defines the behavior of the window.
    [in] HWND hWnd : A handle to the window.
    [in] UINT uMsg : The message.
    [in] WPARAM wParam : Additional message information.
    [in] LPARAM lParam : Additional message information.
    */

    HDC hdc;        // A handle to the display device context of the window.
    PAINTSTRUCT ps; // A structure that contains information for an application.
    TCHAR greeting[] = _T("Hello, Windows desktop!");

    /* [Keyboard and Mouse Input](https://learn.microsoft.com/zh-cn/windows/win32/inputdev/user-input) */
    switch (message) {
        case WM_PAINT: // The WM_PAINT message is sent when the system or another application makes a request to paint a portion of an application's window.
            hdc = BeginPaint(hWnd, &ps);
            TextOut(hdc, 50, 5, greeting, _tcslen(greeting));
            EndPaint(hWnd, &ps);
            break;
        case WM_LBUTTONDOWN: // The WM_LBUTTONDOWN message is posted when the user presses the left mouse button while the cursor is in the client area of a window.
            MessageBox(NULL, _T("Mouse Left Button Clicked!"), _T("Mouse Click"), MB_OK);
            break;
        case WM_RBUTTONDOWN: // The WM_RBUTTONDOWN message is posted when the user presses the right mouse button while the cursor is in the client area of a window.
            MessageBox(NULL, _T("Mouse Right Button Clicked!"), _T("Mouse Click"), MB_OK);
            break;
        case WM_KEYDOWN: // The WM_KEYDOWN message is posted to the window with the keyboard focus when a nonsystem key is pressed.
            MessageBox(NULL, _T("Key Pressed!"), _T("Key Press"), MB_OK);
            break;
        case WM_CLOSE: // The WM_CLOSE message is sent as a signal that a window or an application should terminate.
            if (MessageBox(hWnd, _T("Are you sure you want to close this window?"), _T("Close Window"), MB_YESNO) == IDYES) {
                DestroyWindow(hWnd);
            }
            break;
        case WM_DESTROY: // The WM_DESTROY message is sent when a window is being destroyed.
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
            break;
    }

    return 0;
}