#include <iostream>

using namespace std;

void towersOfHanoi(int n, int x, int y, int z) {
    if (n > 0) {
        towersOfHanoi(n-1, x, z, y);
        cout << "Move top disk from tower " << x << " to top of tower " << y << endl;
        towersOfHanoi(n-1, z, y, x);
    }
}

int main() {
    towersOfHanoi(2, 1, 2, 3);
    return 0;
}