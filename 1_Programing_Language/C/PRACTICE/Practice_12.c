#include<stdio.h>
int main()
{
    int num,n,sum=0,i,tmp;
    scanf("%d%d",&num,&n);
    tmp=num;
    for(i=0;i<n;i++)
    {
        sum+=num;
        num=num*10+tmp;
    }
    printf("%d\n",sum);
    return 0;
}