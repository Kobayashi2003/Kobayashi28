#include <iostream>
#include "valid_parentheses.h"

string boolToString(bool input) {
    return input ? "true" : "false";
}

int main() {
    string s;
    while (cin >> s) {
        bool ret = isValid(s);
        string out = boolToString(ret);
        cout << out << endl;
    }
    return 0;
}