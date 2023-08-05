//为毛你要用递归？？？
#include<stdio.h>
#include<string.h>
#define N 10
int Pow(int x, int y) 
{
    if(y!=0)for(int i=1;i<y;i++)x*=x;
    else x=1;
    return x;
}
void Transform(char *str,int num,int n)
{
    *str=((num%Pow(10,n+1))/Pow(10,n))+'0';

    if(num-Pow(10,n+1)>0)
        Transform(++str,num,++n);
}
int main()
{
    int num;
    char str[N]={'\0'};
    scanf("%d",&num);
    Transform(str,num,0);
    for(int i=strlen(str)-1;i>=0;i--)
        printf("%c ",str[i]);
    return 0;
}