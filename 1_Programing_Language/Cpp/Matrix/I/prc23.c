#include <stdlib.h>

int minPosNumberDisappeared(int* numbers, int n) {
    int res = 0;
    int * tmp = (int *)malloc(sizeof(int) * n);

    for (int i = 0; i < n; i++) {
        if (numbers[i] > 0 && numbers[i] <= n) {
            tmp[numbers[i] - 1] = 1;
        }
    }

    for (int i = 0; i < n; i++) {
        if (tmp[i] == 0) {
            res = i + 1;
            break;
        }
    }

    free(tmp);

    return res == 0 ? n + 1 : res;
}