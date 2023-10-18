#include <stdio.h>
#include <string.h>

#define MAX_LEN 10000

int main() {

    char str[MAX_LEN] = {0};
    int move[MAX_LEN] = {0};

    scanf("%[^\n]", str);
    int len = strlen(str);
    for (int i = 0; i < len; ++i) {
        scanf("%d", &move[i]);
    }

    for (int i = 0; i < len; ++i) {
        char ch = str[i];
        if (ch >= 'A' && ch <= 'Z') {
            ch = (ch - 'A' + move[i]) % 26 + 'A';
        } else if (ch >= 'a' && ch <= 'z') {
            ch = (ch - 'a' + move[i]) % 26 + 'a';
        }
        str[i] = ch;
    }

    printf("%s\n", str);


    return 0;
}