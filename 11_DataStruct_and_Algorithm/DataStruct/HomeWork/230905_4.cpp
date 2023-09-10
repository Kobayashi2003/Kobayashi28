#include <iostream>
#include <vector>
#include <string>

using namespace std;

void solve(int M, int N, vector<int> & num) {

    for (int i = M; i >= 0; --i) {
        if (num.size() != 0 && num[num.size() - 1] < i) {
            if (N == 1)
                return;
            continue;
        }
        num.push_back(i);
        if (N == 1) {
            for (auto i : num)
                cout << i;
            cout << endl;
            num.pop_back();
            return;
        } else {
            solve(M - i, N - 1, num);
        }
        num.pop_back();
    }

    return;
}

int main() {

    int t; cin >> t;
    while (t--) {
        int M, N; cin >> M >> N;
        vector<int> num;
        solve(M, N, num);
    }

    return 0;
}