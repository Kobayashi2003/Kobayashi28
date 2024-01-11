#include <iostream>
#include <vector>

using namespace std;

template <typename Comparable>
Comparable median3(vector<Comparable> & a, int left, int right) {
    int center = (left + right) / 2;
    if (a[center] < a[left])
        swap(a[left], a[center]);
    if (a[right] < a[left])
        swap(a[left], a[right]);
    if (a[right] < a[center])
        swap(a[center], a[right]);
    
    swap(a[center], a[right - 1]);
    return a[right - 1];
}

template <typename Comparable>
void quickSort(vector<Comparable> & a, int left, int right) {
    if (left >= right)
        return;
    Comparable pivot = median3(a, left, right);
    int i = left, j = right - 1;
    for ( ; ; ) {
        while (a[++i] < pivot) {}
        while (pivot < a[--j]) {}
        if (i < j)
            swap(a[i], a[j]);
        else
            break;
    }

    swap(a[i], a[right - 1]);

    quickSort(a, left, i - 1);
    quickSort(a, i + 1, right);
}

template <typename Comparable>
void quickSort(vector<Comparable> & a) {
    quickSort(a, 0, a.size() - 1);
}

int main() {

    vector<int> a = {1, 3, 2, 5, 4};

    quickSort(a);

    for (auto i : a)
        cout << i << " ";

    return 0;
}