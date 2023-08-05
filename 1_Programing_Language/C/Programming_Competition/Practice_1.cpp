#include <iostream>

using namespace std;

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) {
        int num1, num2;
        cin >> num1 >> num2;
        cout << ((int)2e6 - num1 - num2) % (int)1e6 << endl;
    }
    return 0;
}