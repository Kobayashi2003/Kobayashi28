#include <stdio.h>

int main() {

    int num; scanf("%d", &num);
    int count_2 = 0, count_5 = 0;
    while (num) {
        int tmp = num;
        while (tmp % 2 == 0) {
            count_2 += 1;
            tmp /= 2;
        }
        while (tmp % 5 == 0) {
            count_5 += 1;
            tmp /= 5;
        }
        num -= 1;
    }
    
    int result = count_2 > count_5 ? count_5 : count_2;
    printf("%d", result);

    return 0;
}