#include<stdio.h>
#define N 101
int main()
{
    double array[N]={0.0},result[2*N]={0.0},num;
    int power,k,i,j;
    scanf("%d",&k);
    for(i=0;i<k;i++)
    {
        scanf("%d",&power);
        scanf("%lf",&array[power]);
    }
    scanf("%d",&k);
    for(i=0;i<k;i++)
    {
        scanf("%d",&power);
        scanf("%lf",&num);
        for(j=0;j<N;j++)
        {
            result[j+power]+=array[j]*num;
        }
    }
    for(i=2*N-1;i>=0;i--)
    {
        if(result[i]!=0.0)
            printf("%.1lfx^%d ",result[i],i);
    }
    return 0;
}


//两个多项式 最高幂次不能超过100 两个多项式的乘积
//k表示非零项的个数  1<=k<=10