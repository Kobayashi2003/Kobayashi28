#include<stdio.h>
int main()
{
    int num,temp;
    scanf("%d",&num); 
    temp=num;

    int a[1000];
    int i=0;     

    while((num/(int)pow(10,i))!=0)     
    {
        a[i]=temp%10;
        if (temp<10)
        {
            a[i]=temp;
        }
        printf("%d",a[i]);
        temp=temp/10;
        i=i+1;
    }

 return 0;
}

