#include<stdio.h>
int main()
{
    int n,k,num;
    printf("请依次输入灯的盏数(1<=n<=500)以及人数(k)\n");
    scanf("%d %d",&n,&k);
    for(int i=0;i<n;i++)
    {
        num=-i;
        for(int j=1;j<=k;j++) 
            if(i%j==0)num*=-1;
        if(num>0)printf("%d ",num);
    }
    return 0;
}