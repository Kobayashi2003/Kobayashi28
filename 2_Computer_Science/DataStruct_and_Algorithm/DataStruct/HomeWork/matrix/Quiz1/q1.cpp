#include <iostream>
#include <string>

using namespace std;

int main() {

    string s; cin >> s;
    int n; cin >> n;

    string tmp1 = s.substr(0, n);
    string tmp2 = s.substr(n, s.size() - n);

    cout << tmp2 << tmp1 << endl;

    return 0;
}