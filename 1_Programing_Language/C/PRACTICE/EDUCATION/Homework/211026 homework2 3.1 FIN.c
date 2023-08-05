#include<stdio.h>
#include<math.h>
int main()
{
    int num, num1;
    scanf_s("%d", &num);

    num1 = num;//用num1储存num的值

    int temp = 0;

    int x;//定义变量x用于记录num每一位上的数字  

    int i=0;//定义i用于记录num的位数

    printf("该数每一位上的数字从低位到高位分别为\n");

    if (num == 0)           //当num==0时，不使其进入while循环，直接输出该特殊情况的结果
    {
        printf("0\n");
        i = 1;
    }

    while (num != 0)//通过循环运算将num中数字的顺序调换
    {
        x = num % 10;
        printf("%d\n", x);

        temp = temp * 10 + x;
        num /= 10;

        i = i + 1;
    }

    printf("该数为%d位数\n", i);

    printf("该数的逆序为\n");

    int y=1;                            
    while (num1 % (int)pow(10, y) == 0&&num1!=0)     //通过循环结构算出逆序计算时丢失的零的个数并将其补齐
    {
        printf("0");
        y = y + 1;
    }

    printf("%d", temp); 

    return 0;
}