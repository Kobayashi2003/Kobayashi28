#include<stdio.h>
#include<string.h>
void Caesar_cipher(char *data, int len, int key) {

    for(int i = 0; i < len; i++) {
        if(data[i] >= 'a' && data[i] <= 'z') {
            data[i] = (data[i] + key - 'a') % 26 + 'a';
        }else if(data[i] >= 'A' && data[i] <= 'Z') {
            data[i] = (data[i] + key - 'A') % 26 + 'A';
        }else if(data[i] >= '0' && data[i] <= '9') {
            data[i] = (data[i] + key - '0') % 10 + '0';
        }
    }
}
int main() {
    char data[] = "ABC abc 123";
    int key = 0;
    printf("Please input the key:");
    scanf("%d", &key);
    int len = sizeof(data)/sizeof(char) - 1;
    Caesar_cipher(data, len, key);
    for(int i = 0; i < len; i++) {
        printf("%c", data[i]);
    }
    return 0;
}