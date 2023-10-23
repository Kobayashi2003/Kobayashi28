#include <stdio.h>

int main() {

    int M, S, T;
    while (scanf("%d %d %d", &M, &S, &T) != EOF) {
        int s1 = 0, s2 = 0;
        for (int i = 1; i <= T; ++i) {
            s1 += 17;
            if (M >= 10) {
                M -= 10;
                s2 += 60;
            } else {
                M += 4;
            } 

            if (s2 > s1) {
                s1 = s2;
            }

            if (s1 >= S) {
                printf("Yes\n%d\n", i);
                break;
            }
        }

        if (s1 < S) {
            printf("No\n%d\n", s1);
        }

    }

    return 0;
}