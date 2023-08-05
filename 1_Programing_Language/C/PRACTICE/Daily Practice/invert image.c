#include<stdio.h>
int main()
{
    char str[2000]={'\0'};
    int count=0;
    for(int i=0;(str[i]=getchar())!='\n';i++)
        count++;
    for(int i=count-1;i>=0;i--) 
        printf("%c",str[i]);
    return 0;
}

