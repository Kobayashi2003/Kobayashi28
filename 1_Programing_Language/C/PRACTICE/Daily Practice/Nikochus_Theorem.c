//尼科彻斯定理
#include<stdio.h>
#include<math.h>
void Nikochus_Theorem(int num,int initial)
{
    int sum=0,count=0;
    for(int i=initial;sum<pow(num,3);i+=2,count++)
        sum+=i;
    if(sum==pow(num,3)&&count==num)
        for(int i=initial;sum>0;i+=2,sum-=i)
            printf("%d ",i);
    else Nikochus_Theorem(num,initial+=2);
}
int main()
{
    int num;
    scanf("%d",&num);
    Nikochus_Theorem(num,1);
    return 0;
}