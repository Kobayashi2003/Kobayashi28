#include <stdio.h>
#define N 10

int main() {

    int m[N][N] = { 0, };
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) {
            int num; scanf("%d", &num);
            if (num > 0)
                m[i][j] = num;
        }

    for (int j = 0; j < N; ++j) {
        for (int i = 0; i < N; ++i)
            printf("%d ", m[i][j]);
        printf("\n");
    }
    
    return 0;
}