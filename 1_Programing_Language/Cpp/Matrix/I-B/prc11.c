#include <stdio.h>
#include <string.h>

#define MAX_LEN 10000

int MaxLen(char * str, char * T, int str_len, int T_len) {
    int max_len = 0;
    for (int i = 0; i < str_len; ++i) {
        if (str[i] == T[0]) {
            int j = 0;
            while (j < T_len && str[i + j] == T[j]) {
                ++j;
            }
            if (j == T_len) {
                int cur_len = T_len;
                for (int k = i + T_len; k < str_len; ++k) {
                    int k_t = k % T_len;
                    if (str[k] == T[k_t]) {
                        ++cur_len;
                    } else {
                        break;
                    }
                }
                if (cur_len > max_len) {
                    max_len = cur_len;
                }
            }
        }
    }

    return max_len;
}



int main() {

    int N; scanf("%d", &N);

    for (int i = 0; i < N; ++i) {
        char str[MAX_LEN] = {0}; scanf("%s", str);
        char T[MAX_LEN] = {0}; scanf("%s", T);
        printf("%d\n", MaxLen(str, T, strlen(str), strlen(T)));
    }

    return 0;
}