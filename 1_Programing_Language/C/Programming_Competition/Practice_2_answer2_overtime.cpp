#include <iostream>

using namespace std;

using LLI = long long int;

int main() {
    int T; cin >> T;
    while (T--) {
        int N, M; cin >> N >> M;
        LLI R = 0, C = 0, D = 0, omd = 0;
        while (M--) {
            char command; cin >> command;
            if (command == 'R') {
                int x; cin >> x;
                if (R & (1LL << x)) {
                    R ^= (1LL << x);
                    if (C & (1LL << x)) {
                        omd -= 1;
                    }
                } else {
                    R |= (1LL << x);
                    if (C & (1LL << x)) {
                        omd += 1;
                    }
                }
            } else if (command == 'C') {
                int x; cin >> x;
                if (C & (1LL << x)) {
                    C ^= (1LL << x);
                    if (R & (1LL << x)) {
                        omd -= 1;
                    }
                } else {
                    C |= (1LL << x);
                    if (R & (1LL << x)) {
                        omd += 1;
                    }
                }
            } else if (command == 'D') {
                D = 1 - D;
            }
            LLI lighting = N*(__builtin_popcountll(R) + __builtin_popcountll(C)) - 2*__builtin_popcountll(R)*__builtin_popcountll(C) + D*(N - 2*(__builtin_popcountll(R) + __builtin_popcountll(C) - 2*omd));
            cout << lighting << endl;
        }
    }
    return 0;
}