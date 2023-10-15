#include <stdio.h>

#define N 3

int main() {

    int arr[N][N];
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j <N ; ++j) {
            scanf("%d",&arr[i][j]);
        }
    }

    double total = 0;
    for (int i = 0; i < N; ++i) {
        double sum = 0;
        for (int j = 0; j < N; ++j) {
            sum += arr[i][j];
            total += arr[i][j];
        }
        printf("%.2lf ",sum);
    }
    printf("\n%.2lf ", total / N);

    for (int j = 0; j < N; ++j) {
        double sum = 0;
        for (int i = 0; i < N; ++i) {
            sum += arr[i][j];
        }
        printf("%.2lf ",sum / N);
    }
    printf("\n");

    return 0;
}