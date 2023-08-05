#include<iostream>

using namespace std;

void Min(int *nums, int len) {
    int min = nums[0];
    for(int i = 0; i < len; ++i) {
        if (nums[i] < min) {
            min = nums[i];
        }
    }
    cout << min << endl;
}

void Min(double *nums, int len) {
    double min = nums[0];
    for(int i = 0; i < len; ++i) {
        if (nums[i] < min) {
            min = nums[i];
        }
    }
    cout << min << endl;
}

void Min(float *nums, int len) {
    float min = nums[0];
    for(int i = 0; i < len; ++i) {
        if (nums[i] < min) {
            min = nums[i];
        }
    }
    cout << min << endl;
}

void Min(long *nums, int len) {
    long min = nums[0];
    for(int i = 0; i < len; ++i) {
        if (nums[i] < min) {
            min = nums[i];
        }
    }
    cout << min << endl;
}

int main() {
    int a[6] = {2, 22, 0, -6, 67, -111};

    double b[8] = {2.2, 62, -6.1, 500, 68.2, -500.345, -8, 1000};

    float c[4] = {3.2, -8.61, 699, 33};

    long d[3] = {3265891L, 14789L, -63256L};

    Min(a, 6);
    Min(b, 8);
    Min(c, 4);
    Min(d, 3);
    return 0;
}