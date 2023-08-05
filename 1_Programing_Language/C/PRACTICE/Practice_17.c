#include<stdio.h>
int main()
{
    int num,i,cont=0,tmp=3;
    for(num=3;cont<=20;num++)
    {
        for(i=2;i<num;i++)
        {
            if(num%i==0) break;
        }
        if(i==num)
        {
            if(num-tmp==2)
            {
                printf("%d %d\n",tmp,num);
                cont++;
            }
            tmp=num;
        }
        
    }
    return 0;
}