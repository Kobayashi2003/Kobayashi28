#include <stdio.h>
#include <string.h>

#define MAX_LEN 1024


int indexOf(char* str, char* T, int len1, int len2) {
    int next[len2 + 1];
    next[0] = -1;
    int i = 0, j = -1;
    while (i < len2) {
        if (j == -1 || T[i] == T[j]) {
            ++i;
            ++j;
            next[i] = j;
        } else {
            j = next[j];
        }
    }
    i = 0, j = 0;
    while (i < len1 && j < len2) {
        if (j == -1 || str[i] == T[j]) {
            ++i;
            ++j;
        } else {
            j = next[j];
        }
    }
    if (j == len2) {
        return i - j;
    } else {
        return -1;
    }
}

int main() {

    char T[MAX_LEN] = {0}; scanf("%s", T);
    char str[MAX_LEN] = {0}; scanf("%s", str);

    int len1 = strlen(str), len2 = strlen(T);

    int pos = indexOf(str, T, len1, len2);
    printf("%d\n", pos);

    return 0;
}