#include <stdio.h>

int main() {

    int num1, num2; scanf("%d %d", &num1, &num2);
    int ten_digit1 = (num1 / 10) % 10, ten_digit2 = (num2 / 10) % 10;
    int new_num1 = num1 - ten_digit1 * 10 + ten_digit2 * 10;
    int new_num2 = num2 - ten_digit2 * 10 + ten_digit1 * 10;

    printf("%d %d\n", new_num1, new_num2);

    return 0;
}