#include <iostream>
#include <cmath>

using namespace std;

class Solution {

    int n, m;

public:
    Solution() { cin >> n >> m; }

    int solve() {
        // a^2 + 3a - 2(n+m) = 0
        // ans = n - a
        int delta = 9 + 4 * (2 * (n + m));
        int a = (-3 + sqrt(delta)) / 2;
        return n - a;
    }
};

int main() {

    Solution solution;
    cout << solution.solve() << endl;

    return 0;
}