#include <stdio.h>
#include <string.h>

#define MAX_LEN 128

void trim(char *str) {
    int len = strlen(str);
    int i = 0;
    char ch = str[0];

    while (str[i] == ch) {
        i++;
    }

    int j = len - 1;
    while (str[j] == ch) {
        j--;
    }
    
    int k = 0;
    while (i <= j) {
        str[k++] = str[i++];
    }
    str[k] = '\0';
}

int main() {

    char str[MAX_LEN] = {0}; scanf("%[^\n]", str);

    trim(str);

    printf("%s\n", str);

    return 0;
}