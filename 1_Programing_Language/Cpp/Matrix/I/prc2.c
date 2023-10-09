#include <stdio.h>

#define N 3

int main() {

    int m1[N][N] = {0};
    int m2[N][N] = {0};

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; ++j) {
            scanf("%d", &m1[i][j]);
        }
    }
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; ++j) {
            scanf("%d", &m2[i][j]);
        }
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; ++j) {
            printf("%d ", m1[i][j] + m2[i][j]);
        }
        printf("\n");
    }

    return 0;
}