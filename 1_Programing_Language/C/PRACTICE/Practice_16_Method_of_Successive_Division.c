//辗转相除法求最大公约数
#include<stdio.h>
int main()
{
    int num1,num2,tmp;
    scanf("%d%d",&num1,&num2);
    if(num1<num2)
    {
        tmp=num1;
        num1=num2;
        num2=tmp;
    }
    tmp=num1%num2;
    while(tmp)
    {
        num1=num2;
        num2=tmp;
        tmp=num1%num2;
    }
    printf("%d\n",num2);
    return 0;
}