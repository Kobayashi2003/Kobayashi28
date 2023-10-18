#include <stdio.h>

int get_len(int n) {
    int len = 1;
    while (n != 1) {
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        len++;
    }
    return len;
}

int main() {
    int i, start, end, max = 0, tmp;
    scanf("%d%d", &start, &end);
    for (i = start; i <= end; i++) {
        tmp = get_len(i);
        max = tmp > max ? tmp : max;
    }
    printf("%d\n", max);
    return 0;
}
