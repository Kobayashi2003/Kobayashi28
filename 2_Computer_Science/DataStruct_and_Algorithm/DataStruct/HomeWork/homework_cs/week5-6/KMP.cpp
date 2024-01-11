#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<int> make_next(string p);
vector<int> make_nextval(string p);


vector<int> KMP(string s, string p) {

    vector<int> pos;

    int n = s.size();
    int m = p.size();
    vector<int> next = make_next(p);
    vector<int> nextval = make_nextval(p);

    cout << "next:\t\t";
    for (int i = 0; i < next.size(); i++) {
        cout << next[i] << "\t";
    }
    cout << endl;

    cout << "nextval:\t";
    for (int i = 0; i < nextval.size(); i++) {
        cout << nextval[i] << "\t";
    }
    cout << endl;

    for (int i = 0, j = 0; i < n; i++) {
        while (j > 0 && s[i] != p[j]) {
            j = nextval[j];
        }
        if (s[i] == p[j]) {
            j++;
        }
        if (j == m) {
            pos.push_back(i - m + 1);
            j = nextval[j];
        }
    }

    return pos;
}


vector<int> make_next(string patt) {
    vector<int> next(patt.size(), 0);
    next[0] = -1;
    int i = 0, j = -1;
    while (i < patt.size() - 1) {
        if (j == -1 || patt[i] == patt[j]) {
            i++; j++;
            next[i] = j;
        } else {
            j = next[j];
        }
    }

    return next;
}

vector<int> make_nextval(string p) {
    vector<int> nextval = make_next(p);
    for (int i = 0; i < nextval.size(); i++) {
        if (p[i] == p[nextval[i]]) {
            nextval[i] = nextval[nextval[i]];
        }
    }

    return nextval;
}


int main() {

    string s = "";
    string p = "abcaabbabcabaacbacba";

    vector<int> pos = KMP(s, p);
    cout << "pos: ";
    if (pos.size() == 0) {
        cout << "no match";
    } else {
        for (auto i : pos) {
            cout << i << " ";
        }
    }
    cout << endl;

    return 0;
}