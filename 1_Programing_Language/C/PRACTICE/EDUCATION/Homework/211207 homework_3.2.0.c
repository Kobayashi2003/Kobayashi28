#include<stdio.h>
#include<string.h>
#include<malloc.h>
const char *symbol[]={"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"};
const int value[]={31,28,31,30,31,30,31,31,30,31,30,31};
int main()
{
    int sum=0;
    char *str=(char*)malloc(sizeof(char)*3);
    scanf("%s",str);
    for(int i=0;i<12;i++)
        if(strcmp(str,symbol[i])==0)sum+=value[i];
    printf("%d\n",sum);
    return 0;
}