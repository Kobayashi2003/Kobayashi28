//任意一个大于2的偶数都可以表示为两素数之和
#include<stdio.h>
#include<math.h>
void Prime_Numbers(int num,int pris[])
{
    int temp=0,pri,count=0;
    for(pri=2;pri<=num;pri++)
    {
        for(int k=2;k<=sqrt(pri);k++)
            if(pri%k==0)temp++;
        if(temp==0)pris[count++]=pri;
        temp=0;
    }
    for(int i=0;i<count;i++)
        for(int j=0;j<count;j++)
            if(pris[i]+pris[j]==num)printf("%d=%d+%d\n",num,pris[i],pris[j]);
}
int main()
{
    int num,pris[1000]={0};
    scanf("%d",&num);
    Prime_Numbers(num,pris);
    return 0;
}