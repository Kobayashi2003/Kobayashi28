#include<stdio.h>
void elements(int num,int n)
{
    int sum=0;
    for(int elt=1;elt<num;elt++)
    {if(num%elt==0)
        {sum+=elt;
        if(n==1)
        printf("%d ",elt);
        }
     if(n==1&&elt==num-1)putchar('\n');
    }
    if(sum==num&&n==0) 
        {printf("%d,the elements:",num);
         elements(num,1);
        }
}
int main()
{for(int num=1;num<=1000;num++)
    elements(num,0);
 return 0;
}