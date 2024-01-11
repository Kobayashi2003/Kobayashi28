#include <vector>

using namespace std;

// mergeSort algorithm (driver)
template <typename Comparable>
void mergeSort(vector<Comparable> & a)
{
    vector<Comparable> tmpArray(a.size());

    mergeSort(a, tmpArray, 0, a.size() - 1);
}


/* 
    * Internal method that makes recursive calls.
    * a is an array of Comparable items.
    * tmpArray is an array to place the merged result.
    * left is the left-most index of the subarray.
    * right is the right-most index of the subarray.
*/
template <typename Comparable>
void mergeSort( vector<Comparable> & a, vector<Comparable> & tmpArray, int left, int right) {
    if (left < right) {
        int center = (left + right) / 2;
        mergeSort(a, tmpArray, left, center);
        mergeSort(a, tmpArray, center + 1, right);
        merge(a, tmpArray, left, center + 1, right);
    }
}


/* 
    * Internal method that merges two sorted halves of a subarray.
    * a is an array of Comparable items.
    * tmpArray is an array to place the merged result.
    * leftPos is the left-most index of the subarray.
    * rightPos is the index of the start of the second half.
    * rightEnd is the right-most index of the subarray.
*/
template <typename Comparable>
void merge( vector<Comparable> & a, vector<Comparable> & tmpArray, int leftPos, int rightPos, int rightEnd) {
    int leftEnd = rightPos - 1;
    int tmpPos = leftPos;
    int numElements = rightEnd - leftPos + 1;

    // main loop
    while (leftPos <= leftEnd && rightPos <= rightEnd) {
        if (a[leftPos] <= a[rightPos]) {
            tmpArray[tmpPos++] = a[leftPos++];
        } else {
            tmpArray[tmpPos++] = a[rightPos++];
        }
    }

    while (leftPos <= leftEnd) { // copy rest of first half
        tmpArray[tmpPos++] = a[leftPos++];
    }

    while (rightPos <= rightEnd) { // copy rest of right half
        tmpArray[tmpPos++] = a[rightPos++];
    }

    for (int i = 0; i < numElements; i++, rightEnd--) { // copy tmpArray back
        a[rightEnd] = tmpArray[rightEnd]; 
    }
}