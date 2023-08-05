#include<stdio.h>
int main()
{
    int a,b,c,d,x;                                                              //定义a,b,c,d,x
    printf("请输入高等数学、程序设计基础、机械制图、体育共四门科目的成绩\n");       
    scanf("%d,%d,%d,%d",&a,&b,&c,&d);                                           //输入a,b,c,d的值
    x=a+b+c+d;                                                                  //将a+b+c+d的值赋给x
    printf("总成绩=%d",x);                                                      //输出x的值
    return 0;
}
