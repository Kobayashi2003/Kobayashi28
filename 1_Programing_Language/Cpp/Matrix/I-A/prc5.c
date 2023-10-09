#include <stdio.h>

int main() {

    int num1, num2; scanf("%d %d", &num1, &num2);

    int hundreds1 = num1 / 100;
    int hundreds2 = num2 / 100;

    int n_num1 = num1 - hundreds1 * 100 + hundreds2 * 100;
    int n_num2 = num2 - hundreds2 * 100 + hundreds1 * 100;

    printf("%d %d", n_num1, n_num2);

    return 0;
}