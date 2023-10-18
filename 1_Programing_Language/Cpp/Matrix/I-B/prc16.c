#include <stdio.h>

void shift(int *, int , int );

void shift(int * arr, int m, int n)
{
    int i, j, temp;
    for (i = 0; i < n; i++)
    {
        temp = arr[m-1];
        for (j = m-1; j > 0; j--)
            arr[j] = arr[j-1];
        arr[0] = temp;
    }
}

int main()
{
    int A[1010];
    int m, n, i;
    scanf("%d", &m);
    for (i = 0; i < m; i++)
        scanf("%d", &A[i]);
    scanf("%d", &n);
    shift(A, m, n);
    for (i = 0; i < m-1; i++)
        printf("%d ", A[i]);
    printf("%d\n", A[m-1]);
    return 0;
}