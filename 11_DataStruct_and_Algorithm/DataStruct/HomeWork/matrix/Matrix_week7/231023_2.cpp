#include <iostream>
#include <vector>

const int MAX = 10000;

using namespace std;

int main() {

    int table[MAX] = {false};

    int N; cin >> N;
    int overHalf = 0;

    for (int i = 0; i < N; i++) {
        int num; cin >> num;
        table[num]++;
        if (table[num] > N / 2) {
            overHalf = num;
        }
    }

    cout << overHalf << endl;

    return 0;
}