#include<stdio.h>
int main()
{
    int i,t,x;                  //定义变量i,t,x
    scanf("%d",&x);             //输入x的值
    t=1;                        //将1赋给t
    i=3;                        //将3赋给i
    while(i<=x)                 //当满足i<=x时，进入循环结构进行计算
    {
        t=t*i;                  //将t*i的值赋给t
        i=i+2;                  //将i+2的值赋给i
    }
    printf("%d",t);             //输出t的值
    return 0;
}