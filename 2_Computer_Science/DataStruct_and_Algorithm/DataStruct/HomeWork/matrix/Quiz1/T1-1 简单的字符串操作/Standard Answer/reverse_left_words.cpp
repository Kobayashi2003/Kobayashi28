#include <iostream>
using namespace std;

string reverseLeftWords(string s, int n);

int main() {
    string s;
    int n;
    cin >> s >> n;
    cout << reverseLeftWords(s, n);
    return 0;
}

string reverseLeftWords(string s, int n) {
    int len = s.size();
    s += s;
    return s.substr(n, len);
}