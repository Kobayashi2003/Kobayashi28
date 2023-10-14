#include <stdio.h>
#include <string.h>

int main() {

    char str1[21], str2[21];
    scanf("%s", str1); scanf("%s", str2);

    int len1 = strlen(str1), len2 = strlen(str2);

    int cmp = strcmp(str1, str2);
    char chCmp = cmp > 0 ? '>' : (cmp < 0 ? '<' : '='); 

    printf("%s %c %s\n", str1, chCmp, str2);

    return 0;
}