#include<stdio.h>
#include<math.h>
int main()
{
    int i,num;
    double k;
    scanf_s("%d",&num);
    while(num>0)
    { 
        k=sqrt((double)num);
        for(i=2;i<k;i++)
        {
            if(num%i==0)
            break;
        }
        if(i>k)
        printf("%d\n",num);
        num=num-1;
    }
    return 0;
}