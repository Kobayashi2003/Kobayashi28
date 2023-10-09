#include <stdio.h>

int main() {

    int price, num, sum;
    for (int i = 0; i < 2; i++) {
        scanf("%d %d", &price, &num);
        sum += price * num;
    }
    printf("%d\n", sum);

    return 0;
}