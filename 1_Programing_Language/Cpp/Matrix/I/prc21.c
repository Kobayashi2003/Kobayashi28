int maxFood(int a[], int len) {
    int max = a[0];
    for (int i = 1; i < len; ++i) {
        a[i] = a[i-1] + a[i];
        if (a[i] < 0) {
            a[i] = 0;
        }
        if (a[i] > max) {
            max = a[i];
        }
    }

    return max;
}