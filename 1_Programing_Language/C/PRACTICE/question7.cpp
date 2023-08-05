#include <iostream>

using namespace std;

int main() {

    int n; cin >> n;

    int count1 = 0;
    for (int i = 0; i < n; ++i) {
        int num; cin >> num;
        int count2 = 0;
        while (num) {
            num /= 10; count2++;
        }
        if (count2 % 2 == 0) {
            count1 += 1;
        }
    }
    cout << count1 << endl;

    return 0;
}