#include <stdio.h>
#include <string.h>

int main() {

    char str[128]; scanf("%s", str);
    char newStr[128] = {0};

    char lastChar = str[0];
    int count = 1;
    for (int i = 1; str[i] != '\0'; i++) {
        if (str[i] == lastChar) {
            count++;
        } else {
            sprintf(newStr, "%s%c%d", newStr, lastChar, count);
            lastChar = str[i];
            count = 1;
        }
    }
    sprintf(newStr, "%s%c%d", newStr, lastChar, count);

    if (strlen(newStr) < strlen(str)) {
        printf("%s\n", newStr);
    } else {
        printf("%s\n", str);
    }

    return 0;
}