#include<iostream>

using namespace std;

const int DInM[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

void solve() {
    while (true) {
        int m, d;
        cin >> m >> d;
        if (m == 0 && d == 0) {
            break;
        }
        if (m > 12 || m < 1 || d > DInM[m] || d < 1) {
            cout << -1 << endl;
            continue;
        }
        int days = 0;
        for (int i = 1; i < m; ++i) {
            days += DInM[i];
        }
        days += d;
        int date = (days % 7 + 5) % 7;

        // cout << date << endl;

        int after = date <= 4 ? 4 - date : 11 - date;

        if (days + after > 365) {
            cout << -1 << endl;
        } else {
            cout << after << endl;
        }
    }
}

int main() {

    solve();
    return 0;
}