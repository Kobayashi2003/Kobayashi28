#include <vector>
#include <iostream>

using namespace std;

template <typename Comparable>
void merge(vector<Comparable> & v, vector<Comparable> & tmpArray, int leftPos, int rightPos, int rightEnd) {

    int leftEnd = rightPos - 1;
    int tmpPos = leftPos;
    int numElements = rightEnd - leftPos + 1;

    while (leftPos <= leftEnd && rightPos <= rightEnd) {
        if (v[leftPos] <= v[rightPos])
            tmpArray[tmpPos++] = v[leftPos++];
        else
            tmpArray[tmpPos++] = v[rightPos++];
    }

    while (leftPos <= leftEnd)
        tmpArray[tmpPos++] = v[leftPos++];

    while (rightPos <= rightEnd)
        tmpArray[tmpPos++] = v[rightPos++];

    for (int i = 0; i < numElements; ++i, --rightEnd)
        v[rightEnd] = tmpArray[rightEnd];

}

template <typename Comparable>
void mergeSort(vector<Comparable> & v) {
    vector<Comparable> tmpArray(v.size());
    int n = v.size();

    for (int splitSize = 1; splitSize < n; splitSize *= 2) {
        for (int i = 0; i < n; i += splitSize*2) {
            int leftPos = i;
            int rightPos = i + splitSize;
            int rightEnd = min(i + splitSize*2 - 1, n - 1);
            merge(v, tmpArray, leftPos, rightPos, rightEnd);
        }
    }

}

int main() {

    vector<int> v = { 1, 3, 5, 7, 9, 2, 4, 6, 8, 10 };
    mergeSort(v);

    for (auto i : v)
        cout << i << " ";


    return 0;
}