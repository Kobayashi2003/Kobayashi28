#include<stdio.h>
#include<stdlib.h>

void validMountainArray(int* arr, int len) {
    int f2b = 0, b2f = 0;

    for (int i = 0; i < len - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            f2b = i;
            break;
        }
    }
    
    for (int i = len - 1; i > 0; i--) {
        if (arr[i] > arr[i - 1]) {
            b2f = i;
            break;
        }
    }

    if (f2b == b2f && f2b != 0 && b2f != len - 1) {
        printf("true\n");
    } else {
        printf("false\n");
    }
}


int main()
{
    int n;
    scanf("%d",&n);
    int *numbers = (int*) malloc(sizeof(int)*n);
    for (int i=0;i<n;i++)
    {
        scanf("%d",&numbers[i]);
    }
    validMountainArray(numbers,n);
    free(numbers);
    return 0;
}