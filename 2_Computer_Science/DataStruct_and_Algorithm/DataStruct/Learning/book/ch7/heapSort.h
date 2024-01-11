#ifndef _HEAPSORT_H
#define _HEAPSORT_H

#include <vector>
#include <algorithm>
#include <utility>

using std::vector;

template <typename Comparable>
void percDown(vector<Comparable> & a, int i, int n);

template <typename Comparable>
void heapSort(vector<Comparable> & a) {

    for (int i = a.size() / 2; i >= 0; --i) { // build heap
        percDown(a, i, a.size());
    }
    for (int j = a.size() - 1; j > 0; --j) {
        std::swap(a[0], a[j]); // delete max
        percDown(a, 0, j);
    } 
}

inline int leftChild(int i) { return 2 * i + 1; }

template <typename Comparable>
void percDown(vector<Comparable> & a, int i, int n) {
    int child;
    Comparable tmp;
    for (tmp = std::move(a[i]); leftChild(i) < n; i = child) {
        child = leftChild(i);
        if (child != n - 1 && a[child] < a[child + 1]) 
            ++child;
        if (tmp < a[child])
            a[i] = std::move(a[child]);
        else
            break;
    }
    a[i] = std::move(tmp);
}

#endif