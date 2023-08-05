/*
输入一个整数n
判断该整数为正奇数，正偶数，负奇数或负偶数
数据规模
-2^31<=n<=2^31-1，且n不等于0。

输入样例1
1
输出样例1
positive odd

输入样例2
-2
输出样例2
negative even

提示
输出的末尾应当包含一个换行符（\n）
(-3)%2等于-1
*/
#include<stdio.h>
#include<math.h>

void judge(int num)
{
    num=fabs(num);
    num=num%2;
    if(num==0)
    printf("even\n");
    else
    printf("odd\n");
}

int main()
{
    int num;
    printf("请输入一个非零的整数\n");
    scanf("%d", &num);
    if(num>0)
    {
        printf("positive ");
        judge(num);
    }
    else if(num<0)
    {
        printf("nagetive ");
        judge(num);
    }
}