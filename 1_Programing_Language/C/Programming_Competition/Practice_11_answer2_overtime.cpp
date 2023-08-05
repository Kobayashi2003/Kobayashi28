#include <iostream>
#include <vector>

using namespace std;

// using LLI = long long int;

void solve(vector<int> & S) {
    for (int i = S.size() - 1; i > 0; --i) {
        if (S[i] < S[i-1]) {
            S.erase(S.begin() + i);
            if (i != (int)S.size()) {
                i += 1; continue;
            }
        } else if (S[i] == S[i-1]) {
            S[i-1] += 1;
            S.erase(S.begin() + i);
            if (i != (int)S.size()) {
                i += 1; continue;
            }
        }
    }
    int sum = 0;
    for (auto i : S) {
        sum += i;
    }
    cout << sum << endl;
}


int main() {
    int T; cin >> T;
    while (T--) {
        int N, M; cin >> N >> M;
        int *A = new int[N]{0};
        for (int i = 0; i < N; ++i) {
            cin >> A[i];
        }
        while (M--) {
            int L, R; cin >> L >> R;
            if (!(1 <= L && L <= R && R <= N)) return 0;

            vector<int> S;
            for (int i = L-1; i < R; ++i) {
                S.push_back(A[i]);
            }
            solve(S);
        }
    }
    return 0;
}