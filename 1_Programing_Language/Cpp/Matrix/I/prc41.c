#include <stdio.h>

#define N 3

int main() {

    int mat[N][N];
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j <N ; ++j) {
            scanf("%d",&mat[i][j]);
        }
    }

    int res = mat[0][0] * mat[1][1] * mat[2][2] + mat[0][1] * mat[1][2] * mat[2][0] + mat[0][2] * mat[1][0] * mat[2][1]
            - mat[0][2] * mat[1][1] * mat[2][0] - mat[0][0] * mat[1][2] * mat[2][1] - mat[0][1] * mat[1][0] * mat[2][2];

    printf("%d\n",res);

    return 0;
}