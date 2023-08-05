#include<stdio.h>
int main()
{
    char a;
    scanf("%c",&a);
    if((a<=118&&a>=97)||(a<=86&&a>=65))
        a=a+4;
    else
        a=a-22;
    printf("%c",a);
    return 0;
}