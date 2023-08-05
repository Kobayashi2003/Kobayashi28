#include<stdio.h>
#define N 10
int Stringlengh(char *str)
{
    int lengh=0;
    for(int i=0;str[i];i++)
        lengh++;
    return lengh;
}
int main()
{
    char str[N]={'\0'};
    int len;
    scanf("%s",str);
    len=Stringlengh(str);
    printf("%d",len);
    return 0;
}