#include <stdio.h>

int main() {

    int x, y, z; scanf("%d %d %d", &x, &y, &z);

    if (x < y) {
        x += y;
        y = x - y;
        x -= y;
    }

    if (x < z) {
        x += z;
        z = x - z;
        x -= z;
    }

    if (y < z) {
        y += z;
        z = y - z;
        y -= z;
    }

    printf("%d %d %d\n", x, y, z);

    return 0;
}