template <typename T>
int binarySearch(T a[], int n, const T& x) {
    // Search x in a[0:n-1].
    int left = 0;
    int right = n - 1;
    while (left <= right) {
        int middle = (left + right) / 2;
        if (x == a[middle]) return middle;
        if (x > a[middle]) left = middle + 1;
        else right = middle - 1;
    }
    return -1;
}