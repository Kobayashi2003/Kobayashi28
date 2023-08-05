#include <iostream>
#include <string>

using namespace std;

int main() {
    string str, table = "";
    getline(cin, str);
    int max = 0, cont = 0;
    for (int i = 0; i < (int)str.length(); ++i) {
        for (int j = i; j < (int)str.length(); ++j) {
            if (table.find(str[j]) != string::npos) {
                break;
            }
            table += str[j];
            cont += 1;
        }
        max = max > cont ? max : cont;
        cont = 0;
        table.clear();
    }
    cout << max << endl;
    return 0;
}