//字符型指针数组运用实例：输入一个十进制数，将该数以罗马数字的形式进行输出
#include<stdio.h>
const int value[]={1000,900,500,400,100,90,50,40,10,9,5,4,1};
const char *symbol[]={"M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"};
void intoRoman(int num)
{
    int i;
    while(num)
    {
        for(i=0;i<13;i++)
            if(num>=value[i])
            {
                num-=value[i];
                printf("%s",symbol[i]);
                break;
            }
    }
}
int main()
{
    int num; 
    scanf("%d",&num);
    intoRoman(num);
    return 0;
}