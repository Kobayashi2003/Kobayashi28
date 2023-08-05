//输入两个正整数m和n，求其最大公约数和最小公倍数
#include<stdio.h>
int min_(int m,int n) 
{
    int min;
    min=m<n?m:n;
    return min;
}

int max_(int m,int n) 
{
    int max;
    max=m>n?m:n;
    return max;
}

int main()
{
    int cd,cm; //common_divisor,common_multiple

    int m,n;

    scanf("%d,%d",&m,&n);

    int min,max;
    min=min_(m,n);
    max=max_(m,n);

    int div=min;
    
    for(;div>=1;div--)
    {
        if(m%div==0&&n%div==0)
        {
            cd=div;
            printf("The common dvisor is %d\n",cd);
            break;
        }
    }

    int temp_cm=m*n;
    int mul=max;

    for(;mul<=temp_cm;mul++)
    {
        if(mul%m==0&&mul%n==0)
        {
            cm=mul;
            printf("The common multipul is %d\n",cm);
            break;
        }
    }

    return 0;
}
