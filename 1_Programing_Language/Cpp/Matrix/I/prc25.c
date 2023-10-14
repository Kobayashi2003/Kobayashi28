#include <stdio.h>
#include <string.h>

int main() {

    char bigNum1[512]; scanf("%s", bigNum1);
    char bigNum2[512]; scanf("%s", bigNum2);
    unsigned len1 = strlen(bigNum1);
    unsigned len2 = strlen(bigNum2);

    char result[512] = {0};

    int i = len1 - 1, j = len2 - 1, k = 0, carry = 0;

    while (i >= 0 && j >= 0) {
        int tmp = bigNum1[i] - '0' + bigNum2[j] - '0' + carry;
        result[k++] = tmp % 10 + '0';
        carry = tmp / 10;
        i--;
        j--;
    }

    while (i >= 0) {
        int tmp = bigNum1[i] - '0' + carry;
        result[k++] = tmp % 10 + '0';
        carry = tmp / 10;
        i--;
    }

    while (j >= 0) {
        int tmp = bigNum2[j] - '0' + carry;
        result[k++] = tmp % 10 + '0';
        carry = tmp / 10;
        j--;
    }

    if (carry != 0) {
        result[k++] = carry + '0';
    }

    for (int i = k - 1; i >= 0; i--) {
        printf("%c", result[i]);
    }

    return 0;
}