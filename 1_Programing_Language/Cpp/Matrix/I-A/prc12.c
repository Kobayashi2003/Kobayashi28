#include <stdio.h>

int main() {


    int x, y; scanf("%d %d", &x, &y);

    if (x > y) {
        x += y;
        y = x - y;
        x -= y;
    }

    int sum = 0;
    for (int i = x; i <= y; ++i) {
        if (!(i & 1))
            sum += i;
    }

    printf("%d\n", -sum);

    return 0;
}