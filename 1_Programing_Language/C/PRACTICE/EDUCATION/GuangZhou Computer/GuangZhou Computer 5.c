/*
已知一个数列的通项公式为 a_n = a_{n-1} + n （n>0） ,数列首项为a_0=1 。
现输入一个整数x，输出数列a_n的前x项和。
数据规模
所有输入数据均满足 1 =< x <= 100 且 x 为整数。

输入样例1
1
输出样例1
1

输入样例2
3
输出样例2
7
提示
输出的末尾应当包含一个换行符（\n）
*/

#include<stdio.h>
int main()
{
    int num;
    scanf("%d",&num);
    int a[101];
    int sum=0;
    a[0]=1;
    for(int i=1;i<=num;i++)
    {
        a[i]=a[i-1]+i-1;
        sum=sum+a[i];
    }
    printf("%d\n",sum);
    return 0;
}