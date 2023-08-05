#include <iostream>
#include <string>

using namespace std;

// stringTools.h
namespace stringTools {
    string padLeft(string str, int n, char padding=' ');
    string padRight(string str, int n, char padding=' ');
    string cpy(string str1, int startIndex=0, int endIndex=-1);
    string cpy(string str1, string str2, int startIndex=0, int endIndex=-1);
    string remove(string str, char c);
    string remove(string str, int);
    string remove(string str, int startIndex, int endIndex);
};

// stringTools.cpp
// #include "stringTools.h"
string stringTools::padLeft(string str, int n, char padding) {
    if (int len = str.length(); len < n) {
        str.insert(0, n - len, padding);
    }
    return str;
}

string stringTools::padRight(string str, int n, char padding) {
    if (int len = str.length(); len < n) {
        str.insert(len, n - len, padding);
    }
    return str;
}

string stringTools::cpy(string str1, string str2, int startIndex, int endIndex) { // copy str1 to str2
    size_t st_startIndex = startIndex >= 0 ? startIndex : str1.length() + startIndex;
    // if (startIndex < 0) return "";
    // size_t st_startIndex = startIndex;
    size_t st_endIndex = endIndex >= 0 ? endIndex : str1.length() + endIndex; 
    if (st_startIndex > st_endIndex || st_startIndex >= str1.length() || st_endIndex >= str1.length()) {
        return "";
    }
    str2 += str1.substr(st_startIndex, st_endIndex - st_startIndex + 1);
    return str2;
}

string stringTools::cpy(string str1, int startIndex, int endIndex) {
    return stringTools::cpy(str1, "", startIndex, endIndex);
}

string stringTools::remove(string str, char c) { // earse all value c in str
    for (size_t i = 0; i < str.length(); i++) {
        if (str[i] == c) {
            str.erase(i, 1);
            i--;
        }
    }
    return str;
}

string stringTools::remove(string str, int index) {
    size_t st_index = index >= 0 ? index : str.length() + index;
    if (st_index >= str.length()) {
        return str;
    }
    str.erase(index, 1);
    return str;
}

string stringTools::remove(string str, int startIndex, int endIndex) {
    size_t st_startIndex = startIndex >= 0 ? startIndex : str.length() + startIndex;
    // if (startIndex < 0) return "";
    // size_t st_startIndex = startIndex;
    size_t st_endIndex = endIndex >= 0 ? endIndex : str.length() + endIndex;
    if (st_startIndex > st_endIndex || st_startIndex >= str.length() || st_endIndex >= str.length()) {
        return str;
    }
    str.erase(startIndex, endIndex - startIndex + 1);
    return str;
}

// main.cpp
int main() {

    while(true) {
        int N; cin >> N;
        if (cin.fail()) {
            break;
        }
        string str; cin >> str;

        switch (N) {
            case 11: {
                int n; cin >> n;
                str = stringTools::padLeft(str, n);
                break;
            }
            case 12: {
                int n; cin >> n;
                char padding; cin >> padding;
                str = stringTools::padLeft(str, n, padding);
                break;
            }
            case 21: {
                int n; cin >> n;
                str = stringTools::padRight(str, n);
                break;
            }
            case 22: {
                int n; cin >> n;
                char padding; cin >> padding;
                str = stringTools::padRight(str, n, padding);
                break;
            }
            case 31: {
                str = stringTools::cpy(str);
                break;
            }
            case 32: {
                int startIndex; cin >> startIndex;
                str = stringTools::cpy(str, startIndex);
                break;
            }
            case 33: {
                int startIndex; cin >> startIndex;
                int endIndex; cin >> endIndex;
                str = stringTools::cpy(str, startIndex, endIndex);
                break;
            }
            case 41: {
                char c; cin >> c;
                str = stringTools::remove(str, c);
                break;
            }
            case 42: {
                int index; cin >> index;
                str = stringTools::remove(str, index);
                break;
            }
            case 43: {
                int startIndex; cin >> startIndex;
                int endIndex; cin >> endIndex;
                str = stringTools::remove(str, startIndex, endIndex);
                break;
            }
        }
        cout << str << endl;
    }
    return 0;
}