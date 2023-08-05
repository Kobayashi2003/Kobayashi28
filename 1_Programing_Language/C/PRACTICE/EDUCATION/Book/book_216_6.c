#include<stdio.h>
#include<string.h>
#define N 10
void Input(char *str)
{
    for(int i=0;(str[i]=getchar())!='\n';i++);
}
void Strcat(char *str_1,char *str_2,int len)
{
    int i=0;
    while((str_1[len++]=str_2[i++]));
}
int main()
{
    char str_1[2*N]={'\0'},str_2[N]={'\0'};//直接用gets()输入也ok
    Input(str_1);
    Input(str_2);
    Strcat(str_1,str_2,strlen(str_1)-1);
    printf("%s\n",str_1);
    return 0;
}