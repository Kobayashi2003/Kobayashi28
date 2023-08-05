#include <stdio.h>
#include <stdlib.h>

int main() {

    int n; scanf("%d", &n);
    int *arr = (int*)malloc(sizeof(int) * n);
    for (int i = 0; i < n; ++i)
        scanf("%d", &arr[i]);
    int sum = 0;
    for (int i = 0; i < n; ++i)
        sum += arr[i];

    printf("%lf", (double)sum / n);   

    free(arr); 

    return 0;
}