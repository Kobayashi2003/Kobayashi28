#include <iostream>

using namespace std;

int main() {

    int capacity; cin >> capacity;

    int N; cin >> N;
    int *size = new int[N] {0,};
    int *price = new int[N] {0,};
    for (int i = 0; i < N; ++i) 
        cin >> size[i] >> price[i];


    int *dp = new int[capacity + 1] {0,};

    for (int i = 0; i < N; ++i) 
        for (int j = capacity; j >= size[i]; --j)
            dp[j] = max(dp[j], dp[j - size[i]] + price[i]);

    cout << dp[capacity] << endl;

    return 0;
}