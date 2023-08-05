/* 双鸭山大学的期中考试结束了，老师决定按同学们的通过题数来给同学评级。老师班上有n个学生，你需要写一个程序，来完成这个评级过程。

对于完成10题的学生，评级为"Perfect"；
完成了7-9题的同学，评级为"Excellent"；
完成3-6题的同学，评级为"Good"；
完成0-2题的同学，老师会告诉他们"Practice makes perfect"。

输入格式
第一行输入一个整数n，表示班级上的学生个数。
随后会有n行输入，每一行会有一个整数x，表示一名学生的完成题数。

输出格式
输出n行，每一行为对应学生的评级。
数据规模
所有的数据均满足 0<n<100,0<=x<=10 且 n,y 均为整数。

输入样例
4
10
7
4
0

输出样例
Perfect
Excellent
Good
Practice makes perfect */

#include<stdio.h>
int main()
{
    int n;
    printf("Please input the number of the students\n");
    scanf("%d",&n);

    int num[100];

    for(int i=0;i<n;i++)
    scanf("%d",&num[i]);

    for(int i=0;i<n;i++)
    {
        if(num[i]==10)
        printf("Perfect\n");

        else if(num[i]>=7&&num[i]<=9)
        printf("Excellent\n");

        else if(num[i]>=3&&num[i]<=6)
        printf("Good\n");

        else
        printf("Practice makes perfect\n");
    }

    return 0;
}
