#include <iostream>

using namespace std;

void solve() {
    int N; cin >> N;
    int *arr = new int[N] {0};
    for (int i = 0; i < N; i++) 
        arr[i] = i + 1;

    while (N > 2) {
        cout << arr[0] << " ";
        int tmp = arr[1];
        for (int i = 2; i < N; i++) {
            arr[i - 2] = arr[i];
        }
        arr[N - 2] = tmp;
        N--;
    }

    cout << arr[0] << " " << arr[1] << endl;
}

int main() {

    int t; cin >> t;
    while (t--) {
        solve();
    }

    return 0;
}