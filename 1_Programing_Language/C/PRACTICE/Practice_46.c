#include<stdio.h>
int main()
{
    char str[] = "helloworld";
    for(int i = 0; i < sizeof(str) / sizeof(char); i++)
    {
        // str[i] |= 32;//转小写
        str[i] ^=32;//转大写
        printf("%c", str[i]);
    }
    return 0;
}