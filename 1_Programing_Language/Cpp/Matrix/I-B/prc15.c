#include <stdio.h>

#define MAX_N 10000

int main() {

    int n = -1, s = -1;
    while (1) {
        scanf("%d%d", &n, &s);
        if (n == 0 && s == 0)
            break;
        int a[MAX_N] = {0}, b[MAX_N] = {0};

        for (int i = 0; i < n; ++i) {
            scanf("%d%d", &a[i], &b[i]);
        }

        int count = 0;
        while (count < n) {
            int flg = 0;
            for (int i = 0; i < n; ++i) {
                if (b[i] != 0 && b[i] <= s) {
                    s += a[i];
                    a[i] = 0; b[i] = 0;
                    flg = 1; 
                    count++;
                }
            }
            if (!flg && count != n) {
                printf("NO\n");
                break;
            }
        }
        if (count == n)
            printf("YES\n");
    }

    return 0;
}