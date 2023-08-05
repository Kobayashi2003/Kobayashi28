#include<stdio.h>
int main()
{
    char a,b;                                   //定义字符型变量a,b
    printf("请输入单个小写字母\n");               
    scanf("%c",&a);                             //输入字符a
    b=a-32;                                     //将字符变量a所对应的ASCII代码与整数32相减后赋给b
    printf("%c\n",b);                           //以字符的形式输出b
    return 0;
}