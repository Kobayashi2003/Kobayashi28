#include <stdio.h>
#include <string.h>

#define MAX_LEN 1024

int main() {
    int n; scanf("%d", &n);

    for (int i = 0; i < n; ++i) {
        char str1[MAX_LEN] = {0}; scanf("%s", str1);
        char str2[MAX_LEN] = {0}; scanf("%s", str2);

        strcat(str1, str2);
        int len = strlen(str1);
        for (int i = len-1; i >= 0; --i) {
            printf("%c", str1[i]);
        }
        printf("\n");
    }

    return 0;
}