#include <iostream>
using namespace std;

int gcd(int x, int y) {
    if (x < y) {
        x += y;
        y = x - y;
        x -= y;
    }
    if (y == 0) {
        return x;
    }
    else {
        return gcd(y, x % y);
    }
}


int main() {
    int N; cin >> N;
    while (N--) {
        int x, y; cin >> x; cin >> y;
        cout << gcd(x, y) << endl;
    }
    return 0;
}