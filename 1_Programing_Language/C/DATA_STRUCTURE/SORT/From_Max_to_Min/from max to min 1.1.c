#include<stdio.h>
int main()
{
    int a[6],temp;
    for(int i=0;i<6;i++)
        {
            scanf("%d",&a[i]);
        }
    for(int i=1;i<=6;i++)
    {
        int n1=0,n2=1;
        part:
        if(a[n1]>a[n2])
        {
            temp=a[n1];
            a[n1]=a[n2];
            a[n2]=temp;
            n1=n1+1;
            n2=n2+1;
            goto part;
        }
        else
        {
            n1=n1+1;
            n2=n2+1;
            if(n2<=6)
            goto part;
        }
    }

    for(int i=0;i<6;i++)
    {
        printf("%d\n",a[i]);
    }  
    
    return 0;
}






