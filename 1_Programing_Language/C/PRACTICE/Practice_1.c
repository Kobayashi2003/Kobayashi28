//请在整数n=742683613984中删除8个数字，使得余下的数字按原次序组成的新数最小。要求如下
//(1)整数n和删除数字的个数“8”在源程序中完成赋值，程序直接输出运行结果
//(2)程序结果输出先后被删除的数字(之间以逗号分隔)和删除后所得的最小数。
//(提示整数n可以以字符数组的方式定义、赋值和处理)
#include<stdio.h>
#include<string.h>
void Cut(char *str,int digit)
{
    char str_1[12]={'\0'},str_2[12]={'\0'};
    for(int i=0;i<12;i++)
    {
        if(i<digit)str_1[i]=str[i];
        if(i>digit)str_2[i-digit-1]=str[i];
    }
    memset(str,'\0',12);//使用sizeof(str)警告原因:此时memset表示的是一个指针变量(参量)的长度，因此会出现异常
    strcat(str,str_1);
    strcat(str,str_2);
}
void Change(char *str,int count)
{
    for(int i=0;i<12;i++)
        if(str[i]>str[i+1])
        {
            Cut(str,i);
            count++;;
            break;
        }
    if(count<8)Change(str,count);
}
int main()
{
    char str[]="742683613984";

    Change(str,0);

    printf("%s\n",str);

    return 0;
}