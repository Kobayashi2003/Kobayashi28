#include<iostream>

using namespace std;

template <typename T>
void Average(T *nums, int len) {
    T sum = 0;
    for(int i = 0; i < len; ++i) {
        sum += nums[i];
    }
    cout << sum / len << endl;
}

int main() {

    int a[5] = {2, 39, -6, 11, -100};

    double b[7] = {72, -6.1, 97, 68.2, -51.3, -8, 1234};

    float c[5] = {-23.43, 0.4, 345.34, 76.2, -43.4};

    long d[3] = {658L, 1489L, -256L};

    Average(a, 5);

    Average(b, 7);

    Average(c, 5);

    Average(d, 3);

    return 0;
}