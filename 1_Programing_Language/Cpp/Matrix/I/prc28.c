#include <stdio.h>


void decode(char *str) {

    int num = 0;
    int flg = 0;
    char new_str[128] = {0};
    int count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        char c = str[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + c - '0';
            flg = 1;
        } else {
            if (flg) {
                // reverse string from num to the char before num
                int i = num;
                int j = count - 1;
                while (i < j) {
                    char tmp = new_str[i];
                    new_str[i] = new_str[j];
                    new_str[j] = tmp;
                    i++;
                    j--;
                }

                flg = 0;
                num = 0;
            }
            new_str[count++] = c;
        }
    }
    if (flg) {
        // reverse string from num to the char before num
        int i = num;
        int j = count - 1;
        while (i < j) {
            char tmp = new_str[i];
            new_str[i] = new_str[j];
            new_str[j] = tmp;
            i++;
            j--;
        }
    }
    for (int i = 0; i < count; i++) {
        str[i] = new_str[i];
    }
    str[count] = '\0';
}


int main() {

    char str[128] = {0};
    scanf("%s", str);

    decode(str);

    printf("%s\n", str);

    return 0;
}