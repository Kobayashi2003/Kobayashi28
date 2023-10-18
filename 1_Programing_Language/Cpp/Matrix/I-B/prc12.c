#include <stdio.h>
#include <string.h>

#define MAX_LEN 10000

int main() {

    char str1[MAX_LEN] = {0}; scanf("%s", str1);
    char str2[MAX_LEN] = {0}; scanf("%s", str2);

    if (strlen(str1) != strlen(str2)) {
        printf("NO\n");
        return 0;
    } 

    int len = strlen(str1);
    int count = 0;
    int dif1 = -1, dif2 = -1;

    for (int i = 0; i < len; ++i) {
        if (str1[i] != str2[i]) {
            ++count;
            if (dif1 == -1) {
                dif1 = i;
            } else {
                dif2 = i;
            }
        }
    }

    if (count == 2 && str1[dif1] == str2[dif2] && str1[dif2] == str2[dif1]) {
        printf("YES\n");
    } else if (count == 0) {
        int flg = 0;
        for (int i = 0; i < 26; ++i) {
            char c = 'a' + i;
            for (int j = 0; j < len; ++j) {
                if (str1[j] == c) {
                    if (flg) {
                        printf("YES\n");
                        return 0;
                    } else {
                        flg = 1;
                    }
                }
            }
            flg = 0;
        }
        printf("NO\n");
    } else {
        printf("NO\n");
    }

    return 0;
}