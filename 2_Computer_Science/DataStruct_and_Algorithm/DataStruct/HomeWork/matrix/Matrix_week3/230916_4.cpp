#include <iostream>
#include <vector>

using namespace std;

int main() {

    int s, n; cin >> s >> n;
    vector<int> v(n);
    for (int i = 0; i < n; ++i) cin >> v[i];

    int min_len = n + 1;
    for (int start = 0; start < n; ++start) {
        int sum = 0, count = 0;
        for (int i = start; i < n; ++i) {
            sum += v[i];
            ++count;
            if (sum >= s)
                min_len = min(min_len, count);
        }
    }

    cout << (min_len == n + 1 ? 0 : min_len) << endl;

    return 0;
}