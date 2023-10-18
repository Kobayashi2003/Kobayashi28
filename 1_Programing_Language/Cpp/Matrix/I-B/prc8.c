#include <stdio.h>
#include <string.h>

void printNumber(const char * str, int len) {
    for (int i = 0; i < len; ++i) {
        if (str[i] >= '0' && str[i] <= '9') {
            printf("%c ", str[i]);
        }
    }
}

int main() {

    char str[100]; scanf("%s", str);
    printNumber(str, strlen(str));

    return 0;
}