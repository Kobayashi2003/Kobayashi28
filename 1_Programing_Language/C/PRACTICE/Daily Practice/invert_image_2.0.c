#include<stdio.h>
#include<string.h>
#define N 10
int main()
{
    char str[N]={'\0'};
    printf("Please enter a string:\n");
    scanf("%s",str);
    printf("The invert image string is:\n");
    for(int i=strlen(str)-1;i>=0;i--)
        printf("%c",str[i]);
    putchar('\n');
    return 0;
}