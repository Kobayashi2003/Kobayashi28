/*
编写一个C程序，输入a、b、c、d 四个数，将这四个数按照从大到小的顺序依次输出。输入和输出都以空格进行分隔
*/
#include<stdio.h>
int main()
{
    int num1,num2,num3,num4,temp;
    printf("请以num1 num2 num3 num4的格式输入4个数字\n");
    scanf("%d %d %d %d",&num1,&num2,&num3,&num4);
    
    for(int j=3;j>=0;j--)
    {
    
        if(num1>num2) //比较输入的四个数中相邻的两个数，并通过对调的方式将较大的数换至前方
        {
            temp=num1; 
            num1=num2;
            num2=temp;
        }
        if(num2>num3) 
        {
            temp=num2; 
            num2=num3;
            num3=temp;
        }
        if(num3>num4) 
        {
            temp=num3; 
            num3=num4;
            num4=temp;
        }
    }
    printf("从大到小排序为\n%d %d %d %d\n",num4,num3,num2,num1);
    
    return 0;
}