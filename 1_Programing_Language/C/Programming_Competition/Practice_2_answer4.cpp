// #include <iostream>
// #include <set>
// #include <limits>
#include <bits/stdc++.h>

using namespace std;

int main() {

    int T; cin >> T;
    while (T--) {
        int N, M; cin >> N >> M;
        set<int> R; // 用于记录有效的 R 指令
        set<int> C; // 用于记录有效的 C 指令
        int D = 0; // 用于记录 D 指令执行的次数
        int omd = 0; // on the main diagonal
        while (M--) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            char command; cin >> command;
            if (command == 'R') {
                int x; cin >> x;
                if (R.find(x) != R.end()) {
                    R.erase(x);
                    if (C.find(x) != C.end()) {
                        omd -= 1;
                    }
                } else {
                    R.insert(x);
                    if (C.find(x) != C.end()) {
                        omd += 1;
                    }
                }
            } else if (command == 'C') {
                int x; cin >> x;
                if (C.find(x) != C.end()) {
                    C.erase(x);
                    if (R.find(x) != R.end()) {
                        omd -= 1;
                    }
                } else {
                    C.insert(x);
                    if (R.find(x) != R.end()) {
                        omd += 1;
                    }
                }
            } else if (command == 'D') {
                D = 1 - D;
            }
            long long int lighting = N*(R.size() + C.size()) - 2*R.size()*C.size() + D*(N - 2*(R.size() + C.size() - 2*omd));
            cout << lighting << endl;
        }
    }
    return 0;
}