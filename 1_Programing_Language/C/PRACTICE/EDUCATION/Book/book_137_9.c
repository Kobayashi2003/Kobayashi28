#include<stdio.h>
int main()
{
    for(int num=1;num<=1000;num++)
    {
        int sum=0;
        for(int element=1;element<num;element++)
        {
            if(num%element==0) sum+=element;
        }
        if(sum==num)printf("%d\n",num);
    }
    return 0;
}