#include <stdio.h>
#include <string.h>

#define MAX_LEN 1024

int main() {

    char str[MAX_LEN] = {0};
    scanf("%s", str);

    int len = strlen(str);

    for (int i = 0; i < len / 2; ++i) {
        if (str[i] != str[len - i - 1]) {
            printf("false\n");
            return 0;
        }
    }

    printf("true\n");

    return 0;
}