/*
Given an odd integer n, please find the rule and print an n x n matrix. 
 Please complete the program according to the input and output examples

Note
Pay attention to outputting the space at the end of each line to satisfy that there are nn characters in each line.

EXAMPLE INPUT 1
5
EXAMPLE OUTPUT 1
1 2 3
 123 
88944
 765 
7 6 5
EXAMPLE INPUT 2
7
EXAMPLE OUTPUT 2
1  2  3
 1 2 3 
  123  
8889444  
  765  
 7 6 5 
7  6  5
 */

//循环三次 1 (0)1(2)2(2)3(0) 2 (1)1(1)2(1)3(1) 3 (2)1(0)2(0)3(2) 8889444 由123将每一行分为四个部分 并将该将矩阵分为上中下三部分进行讨论

#include<stdio.h>
int main()
{
    printf("please input an odd number\n")

    int num;
    scanf("%d",&num);

    int i;//定义变量i用以计算循环所需的次数
    i=(num-1)/2;

    //上部

    for(int x=1;x<=i;x++)
    {
    for(int x2=1;x2<x;x2++)
    {
    printf(" ");
    }

    printf("1");

    for(int x1=1;x1<=i-x;x1++)
    {
    printf(" ");
    }

    printf("2");

    for(int x1=1;x1<=i-x;x1++)
    {
    printf(" ");
    }

    printf("3");

    //中部

    for(int x2=1;x2<x;x2++)
    {
    printf(" ");
    }

    printf("\n");

    }

    for(int n=1;n<=i;n++)
    {
    printf("8");
    }

    printf("9");

    for(int n=1;n<=i;n++)
    {
    printf("4");
    }

    printf("\n");

    //下部

    for(int y=i;y>0;y--)
    {
    for(int x3=1;x3<y;x3++)
    {
    printf(" ");
    }

    printf("7");

    for(int x4=1;x4<=i-y;x4++)
    {
    printf(" ");
    }

    printf("6");

    for(int x4=1;x4<=i-y;x4++)
    {
    printf(" ");
    }

    printf("5");

    for(int x3=1;x3<y;x3++)
    {
    printf(" ");
    }

    printf("\n");
    }

    return 0;
}
