#include <stdio.h>

#define N 5

int main() {

    int num; scanf("%d", &num);


    int count = 0; int digits[N] = {0};
    
    while (num > 0) {
        digits[count] = num % 10;
        num /= 10;
        count++;
    }

    printf("%d\n", count);
    
    for (int i = count-1; i >= 0; i--) {
        printf("%d ", digits[i]);
    }
    printf("\n");

    short zero_head = 1;
    for (int i = 0; i < count; i++) {
        if (digits[i])
            zero_head = 0;
        if (!zero_head)
            printf("%d", digits[i]);
    }


    return 0;
}