// 输出数组中最大数的索引

#include<iostream>

using namespace std;

void findMax(int *arr, int num) {
    int tmp = arr[0], ord = 0;
    for(int i = 0; i < num; ++i) {
        if (arr[i] > tmp) {
            tmp = arr[i];
            ord = i;
        }
    }
    cout << ord << endl;
}

int main() {
    int N;
    cin >> N;
    for(int i = 0; i < N; ++i) {
        int num;
        cin >> num;
        int arr[num];
        for(int j = 0; j < num; ++j) {
            cin >> arr[j];
        }
        findMax(arr, num);
    }
    return 0;
}