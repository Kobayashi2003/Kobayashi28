#include <windows.h>
#include <shlobj.h>
#include <tchar.h>
#include <cstdlib>
#include <cstring>

#include <map>
#include <vector>
#include <string>

#include <filesystem>
#include <fstream>

#include <random>
#include <ctime>

using std::map;
using std::wstring;
using std::vector;

using std::filesystem::directory_iterator;
using std::wifstream;
using std::wofstream;

using C_G_MAP = map<wstring, vector<wstring>>;

static const TCHAR szWindowClass[] = _T("Random GALGAME");
static const TCHAR szTitle[] = _T("Random GALGAME");

HINSTANCE hInst;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
C_G_MAP get_galgame_map(const wstring& gal_folder);
vector<wstring> get_random_gal_list(const C_G_MAP& c_g_map, u_int gal_num);


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASSEX wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(hInstance, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(NULL, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = NULL;
    wcex.lpszClassName = szWindowClass;
    wcex.hIconSm = LoadIcon(wcex.hInstance, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex)) {
        MessageBox(NULL, _T("Call to RegisterClassEx failed!"), _T("Win32 Guided Tour"), NULL);
        return 1;
    }

    hInst = hInstance;

    HWND hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 500, 250, NULL, NULL, hInstance, NULL);

    if (!hWnd) {
        MessageBox(NULL, _T("Call to CreateWindow failed!"), _T("Win32 Guided Tour"), NULL);
        return 1;
    }

    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    static wstring gal_folder;
    static C_G_MAP c_g_map;
    static u_short gal_num = 5;
    static vector<wstring> random_gal_list;

    // read the GALGAME folder from the config file
    if (!std::filesystem::exists(".random_gal_config")) {   // if the config file does not exist,
        wofstream wofs(".random_gal_config");               // then create the config file
        wofs.close();
    } else {                                                // if the config file exists,
        wifstream wifs(".random_gal_config");               // then read the GALGAME folder from the config file
        wifs >> gal_folder;
        wifs.close();
    }

    // if the GALGAME folder is empty, then select the GALGAME folder
    if (gal_folder.empty()) {
        TCHAR szBuffer[MAX_PATH];                       // buffer for the folder path
        BROWSEINFO bi = { 0 };                          // structure for the folder browser
        bi.lpszTitle = _T("Select the GALGAME folder"); // title of the folder browser
        LPITEMIDLIST pidl = SHBrowseForFolder(&bi);     // get the folder path
        if (pidl != 0) {
            SHGetPathFromIDList(pidl, szBuffer);
            // convert TCHAR to WCHAR, then convert WCHAR to wstring
            WCHAR w_szBuffer[MAX_PATH];
            for (int i = 0; i < MAX_PATH; ++i) {
                w_szBuffer[i] = szBuffer[i];
            } 
            gal_folder = wstring(w_szBuffer);
            // write the GALGAME folder to the config file
            wofstream wofs(".random_gal_config");
            wofs << gal_folder;
            wofs.close();
        }
        if (gal_folder.empty()) {
            MessageBox(NULL, _T("Please select the GALGAME folder!"), _T("Error"), MB_OK | MB_ICONERROR);
            return 0;
        }
    }

    switch (message) {
        case WM_CREATE: {   // when the window is created
            c_g_map = get_galgame_map(gal_folder);
            random_gal_list = get_random_gal_list(c_g_map, gal_num);
            break;
        }
        case WM_PAINT: {    // when the window needs to be painted
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            TextOut(hdc, 10, 10, _T("Random GALGAME"), 14);
            for (u_int i = 0; i < random_gal_list.size(); ++i) {
                TextOutW(hdc, 10, 30 + 20 * i, random_gal_list[i].c_str(), random_gal_list[i].size());
            }
            EndPaint(hWnd, &ps);
            break;
        }
        case WM_KEYDOWN:    // when a key is pressed
            if (wParam == VK_RETURN) {      // if input enter, generate new random GALGAME list
                random_gal_list = get_random_gal_list(c_g_map, gal_num);
                InvalidateRect(hWnd, NULL, TRUE);
            }
            else if (wParam == VK_SPACE) {  // if input space, choose a new folder
                wstring tmp_folder;
                TCHAR szBuffer[MAX_PATH];
                BROWSEINFO bi = { 0 };
                bi.lpszTitle = _T("Select the GALGAME folder");
                LPITEMIDLIST pidl = SHBrowseForFolder(&bi);
                if (pidl != 0) {
                    SHGetPathFromIDList(pidl, szBuffer);
                    WCHAR w_szBuffer[MAX_PATH];
                    for (int i = 0; i < MAX_PATH; ++i) {
                        w_szBuffer[i] = szBuffer[i];
                    }
                    tmp_folder = wstring(w_szBuffer);
                }
                if (!tmp_folder.empty()) {
                    gal_folder = tmp_folder;
                    wofstream wofs(".random_gal_config");
                    wofs << gal_folder;
                    wofs.close();
                    c_g_map = get_galgame_map(gal_folder);
                    random_gal_list = get_random_gal_list(c_g_map, gal_num);
                    InvalidateRect(hWnd, NULL, TRUE);
                }
            }
            break;
        case WM_CLOSE:      // when the window is closed
            DestroyWindow(hWnd);
            break;
        case WM_DESTROY:    // when the window is destroyed
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}


C_G_MAP get_galgame_map(const wstring& gal_folder) {
    C_G_MAP c_g_map;
    for (const auto& company : directory_iterator(gal_folder)) {
        vector<wstring> galgame_names;
        for (const auto& galgame : directory_iterator(company.path())) {
            galgame_names.push_back(galgame.path().filename().wstring());
        }
        c_g_map[company.path().filename().wstring()] = galgame_names;
    }
    return c_g_map;
}


vector<wstring> get_random_gal_list(const C_G_MAP& c_g_map, u_int gal_num) {
    std::default_random_engine e(time(0));
    std::uniform_int_distribution<unsigned> u(0, c_g_map.size() - 1);

    vector<wstring> random_gal_list;
    u_short gal_count = 0;
    u_short repeat_count = 0;

    while (gal_count < gal_num) {
        int company_index = u(e);
        auto it = c_g_map.begin();
        std::advance(it, company_index);
        wstring company_name = it->first;
        vector<wstring> gal_names = it->second;

        int gal_index = u(e) % gal_names.size();
        wstring gal_name = gal_names[gal_index];

        wstring company_gal = company_name + L":" + gal_name;
        if (std::find(random_gal_list.begin(), random_gal_list.end(), company_gal) == random_gal_list.end()) {
            random_gal_list.push_back(company_gal);
            gal_count++;
        } else {
            repeat_count++;
            if (repeat_count > 10) {
                MessageBox(NULL, _T("There are not enough gals in the folder, please check the folder."), _T("Error"), NULL);
                break;
            }
        }
    }

    return random_gal_list;
}