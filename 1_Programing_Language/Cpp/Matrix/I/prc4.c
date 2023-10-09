#include <stdio.h>

#define N 5

int main() {

    int arr[N] = {0};

    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }

    int tmp = 0;
    for (int i = 0; i < N; i++) {
        scanf("%d", &tmp);
        printf("%d ", arr[i] + tmp);
    }

    return 0;
}