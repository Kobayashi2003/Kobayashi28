#include <iostream>
#include <string>

using namespace std;


void solve() {

    string str1, str2;
    cin >> str1 >> str2;

    str1 = str1 + str1;
    if (str1.find(str2) != string::npos) {
        cout << "True" << endl;
    } else {
        cout << "False" << endl;
    }
}

int main() {

    int t; cin >> t;
    while (t--) 
        solve();


    return 0;
}