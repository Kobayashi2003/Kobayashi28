#include <iostream>
#include <string>
#include <set>

using namespace std;

int main() {

    string str;
    getline(cin, str);

    // Violent recursion
    int max = 0, cont = 0;
    for(int i = 0; (unsigned long long int)i < str.length(); ++i) {
        set <char> table;
        for (int j = i; (unsigned long long int)j < str.length(); ++j) {
            if (table.find(str[j]) != table.end()) {
                break;
            }
            table.insert(str[j]);
            cont += 1;
        }
        max = max > cont ? max : cont;
        cont = 0;
    }

    cout << max << endl;

    return 0;
}