#include<stdio.h>


void merge(int A[], int m, int B[], int n);

void merge(int A[], int m, int B[], int n) {
    int i = m - 1, j = n - 1, k = m + n -1;
    while (i >= 0 && j >= 0) {
        if (A[i] > B[j]) {
            A[k--] = A[i--];
        } else {
            A[k--] = B[j--];
        }
    }
    while (j >= 0) {
        A[k--] = B[j--];
    }
}


int main()
{
    int a[200], b[200];
    int m, n;
    scanf("%d%d", &m, &n);
    int i;
    for(i=0; i<m; i++){
        scanf("%d", &a[i]);
    }
    for(i=0; i<n; i++){
        scanf("%d", &b[i]);
    }
    merge(a, m, b, n);
    for(i=0; i<m+n; i++){
        printf("%d\n", a[i]);
    }
    return 0;
}
