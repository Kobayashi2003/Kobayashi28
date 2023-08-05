#include<stdio.h>
#include<string.h>
#define N 10
const char symbol[]={'1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'};//定义样例对照表，使每一个出现在symbol中的元素与value数组内的元素对应
const int value[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
int Pow(int x,int y)//自定义一个返回值为int型的pow函数，用于求数的幂
{
    int x_temp=x;
    int i;
    if(y==0)return 1;
    else for(i=1;i<y;i++)x*=x_temp;
    return x;
}
int Change(char *str,int len)
{
    int num=0;
    int i,j,check;
    for(i=len,j=0;i>0;i--,j++)
        for(check=0;check<15;check++)
            if(str[j]==symbol[check])
                num+=value[check]*Pow(16,i-1);//遍历对照表，找出与当前字符对应的元素，并输出value表中对应的数值
    return num;
}
int main()
{
    int num;
    char str[N]={'\0'};
    printf("Please input a HEX number:\n");
    scanf("%s",str);
    strlwr(str);
    num=Change(str,strlen(str));
    printf("Change into DEC:%d\n",num);
    return 0;
}   