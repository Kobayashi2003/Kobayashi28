#include<stdio.h>
int main()
{
    int n;
    printf("Please input a positive integer n (3<=n<=20):");
    scanf("%d", &n);

    for(int i=1;i<=n;i++)
    {
        for(int k=1;k<i;k++)//根据所在层数输出相应个数的空格
            printf(" ");
        for(int j=2*(n-i)+1;j>0;j--)//根据所在层数输出相应个数的'#'
            printf("#");
        putchar('\n');
    }
    
    return 0;
}