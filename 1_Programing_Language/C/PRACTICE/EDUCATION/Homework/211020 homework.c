#include<stdio.h>
int main()
{
    int a,b,c,min;                              //定义变量a,b,c,min
    printf("please in put a,b,c\n");            
    scanf("%d,%d,%d", &a, &b, &c);              //输入a,b,c
    min=a;                                      //将a的值赋给min
    if(min>b)                                   //当min>b时，将b的值赋给min，以下同理
    min=b;
    if(min>c)
    min=c;
    printf("min=%d",min);                       //输出min的值
    return 0;
}

