#include <stdio.h>
#include <stdlib.h>

char* removeZero(char* num) {
    int len = 0;
    while (num[len] != '\0') {
        ++len;
    }
    int i = 0;
    while (num[i] == '0') {
        ++i;
    }
    if (i == len) {
        num[0] = '0';
        num[1] = '\0';
        return num;
    }
    for (int j = 0; j < len - i; ++j) {
        num[j] = num[j + i];
    }
    num[len - i] = '\0';
    return num;
}

char* multiply(const char* num1, const char* num2) {
    int len1 = 0, len2 = 0;
    while (num1[len1] != '\0') {
        ++len1;
    }
    while (num2[len2] != '\0') {
        ++len2;
    }
    int len = len1 + len2;
    char* num = (char*)malloc(sizeof(char) * (len + 1));
    for (int i = 0; i < len; ++i) {
        num[i] = '0';
    }
    num[len] = '\0';
    for (int i = len1 - 1; i >= 0; --i) {
        for (int j = len2 - 1; j >= 0; --j) {
            int mul = (num1[i] - '0') * (num2[j] - '0');
            int sum = num[i + j + 1] - '0' + mul;
            num[i + j + 1] = sum % 10 + '0';
            num[i + j] += sum / 10;
        }
    }
    char * new_num = removeZero(num);
    return new_num;
}

int main(){
	char num1[102];
    char num2[102];
    scanf("%s", num1);
    scanf("%s", num2);
    char* num = multiply(num1, num2);
    printf("%s", num);
    free(num);
	return 0;
}