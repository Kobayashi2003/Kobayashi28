#include <stdio.h>

int main() {

    int num; scanf("%d", &num);

    int count = 0;
    while (num) {
        count += num & 1;
        num >>= 1;
    }

    printf("%d", count);

    return 0;
}