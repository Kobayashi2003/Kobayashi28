/*
输入一个正整数 n， 打印一个等腰三角形，这个三角形有 n 行，第 i (1≤i≤n) 行有 i 个字符，
其中 
i 为奇数时，该行为字符 * ，
i 为偶数时，该行为字符 # 。
对于第 i 行第 j 列字符，如果 i+j 是 5 的倍数，则输出 5，不考虑字符 * #。

数据规模
所有的数据均满足 1≤n≤30。

输入格式
输入共有1行，一个整数 n。

输出格式
见样例，注意不要输出行末空格。
请注意输出应以换行符\n结束。

下面是n=3的例子：
*
##
*5*

*/

#include<stdio.h>
int main()
{
    int n;
    scanf("%d",&n);

    int judge;

    for(int i=1;i<=n;i++)
    {
        judge=i%2==0;

        for(int j=1;j<=i;j++)
        {
            switch(judge)
            {
                case 0:
                    if((i+j)%5==0)
                        printf("5");

                    else
                        printf("*");

                    break;

                case 1:
                    if((i+j)%5==0)
                        printf("5");

                    else
                        printf("#");
                    break;
            }
        }

        putchar('\n');
    }

    return 0;
}