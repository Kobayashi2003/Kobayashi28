#include<stdio.h>
int main()
{
    int a=0;     
    int b=0; 
    int num=0;                              
    printf("输入一个正整数\n");
    scanf("%d",&num);
    while(num>0)
    {
    for(int i=2;i<num;i++) 
    {
         if(num%i==0)  a++;   
        
    }
    if(a==0)
    {
         b=b+1;
         printf("第%d个素数为%d\n",b,num);
    }
    num=num-1;
    a=0;
    }
    return 0;   
}