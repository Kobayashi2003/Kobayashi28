#include <stdio.h>

int main() {

    int x, y; scanf("%d %d", &x, &y);
    int sum = 0;

    if (x > y) {
        int tmp = x;
        x = y;
        y = tmp;
    }

    for (int i = x; i <= y; i++)
        if (i & 1)
            sum += i;
        
    printf("%d", sum);

    return 0;
}