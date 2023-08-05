//水仙花数，又称阿姆斯特朗数
#include<stdio.h>
#include<math.h>
int main()
{
    int num=100;
    for(;num<=999;num++)
    {
        int num_100=num/100,num_10=(num%100)/10,num_1=num%10;
        if(num==pow(num_100,3)+pow(num_10,3)+pow(num_1,3))
            printf("%d\n",num);
    }
    return 0;
}