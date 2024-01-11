#include <iostream>

using namespace std;

double solve(double x, int n, double & res) {
    if (n == 1) {
        res = x;
        return x;
    }
    double lst = solve(x, n-1, res);
    double cur = -lst * x * x / (2*n - 1) / (2*n - 2);
    res += cur;
    return cur;
}

int main() {

    double x; int n; cin >> x >> n;
    double res = 0;
    solve(x, n, res);
    cout << res << endl;

    return 0;
}