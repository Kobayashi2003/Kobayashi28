#include <iostream>
#include <stdlib.h>

using namespace std;

template <typename eT>
int binarySearch(eT* arr, int start, int end, eT target) {
    if (start > end) {
        return -1;
    }
    int mid = (start + end) / 2;
    if (arr[mid] == target) {
        return mid;
    }
    else if (arr[mid] > target) {
        return binarySearch(arr, start, mid - 1, target);
    }
    else {
        return binarySearch(arr, mid + 1, end, target);
    }
}


int main() {

    int length = 1; cin >> length; // length of array
    int *arr_int = new int[length]; // array
    for (int i = 0; i < length; i++) {
        cin >> arr_int[i];
    }
    int target_int = 0; cin >> target_int; // target integer

    cout << binarySearch(arr_int, 0, length - 1, target_int) << endl;

    float *arr_float = new float[length]; // array
    for (int i = 0; i < length; i++) {
        cin >> arr_float[i];
    }
    float target_float = 0; cin >> target_float; // target float

    cout << binarySearch(arr_float, 0, length - 1, target_float) << endl;

    return 0;
}