#include <iostream>

using namespace std;

int main() {

    int M, N;
    cin >> M >> N;
    int *arr1 = new int[M];
    int *arr2 = new int[N];
    for (int i = 0; i < M; i++) {
        cin >> arr1[i];
    }
    for (int i = 0; i < N; i++) {
        cin >> arr2[i];
    }

    auto MIN =  [](int x, int y) {return x < y;};

    int *arr3 = new int[N + M];
    int i = 0, j = 0, ord = 0;
    while (i != M && j != N) {
        if (MIN(arr1[i], arr2[j])) {
            arr3[ord++] = arr1[i++];
        } else {
            arr3[ord++] = arr2[j++];
        }
    }
    while (i != M) {
        arr3[ord++] = arr1[i++];
    }

    while (j != N) {
        arr3[ord++] = arr2[j++];
    }

    for (int i = 0; i < N + M; i++) {
        cout << arr3[i] << " ";
    }
    cout << endl;

    delete arr1, arr2, arr3;

    return 0;
}