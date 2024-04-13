#include <iostream>
#include <string> 

using namespace std;

int main() {

    string str = "hello world and python!";
    while (str.find(" ") != string::npos) {
        int pos = str.find(" ");
        cout << pos << endl;
        str.replace(pos, 1, "|");
    }
    cout << str << endl;

    while (str.find("|") != string::npos) {
        int pos = str.find("|");
        cout << str.substr(0, pos) << endl;
        str = str.substr(pos + 1);
    }
    cout << str << endl;

    return 0;
}