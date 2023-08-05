#include<stdio.h>
void primeNumber(int *p)
{
    int sum=0,num,*tmp=p;
    for(;p<tmp+6;p++)
    {
        for(num=2;num<=*p;num++)
        {
            if(*p%num==0) break;
        }
        if(num!=*p)sum+=*p;
    }
    printf("Prime number sum:%d\n",sum);
}
void sort(int *p1)
{
    int *p2=p1,*tmp=p1;
    printf("sort:");
    for(;p1<tmp+6;p1++)
    {
        for(p2=p1;p2<tmp+6;p2++)
            if(*p1>*p2)
            {
                *p1^=*p2;
                *p2^=*p1;
                *p1^=*p2;
            }
        printf("%d ",*p1);
    }
}
int main()
{
    int matrix[2][3];
    int i,j;
    for(i=0;i<2;i++)
        for(j=0;j<3;j++)
            scanf("%d",&matrix[i][j]);
    printf("Output matrix:\n");
    for(i=0;i<2;i++)
    {
        for(j=0;j<3;j++)
            printf("%d ",matrix[i][j]);
        putchar('\n');
    }
    primeNumber(&matrix[0][0]);
    sort(&matrix[0][0]);
    return 0;
}
/*编写两个函数（数组作为函数参数）：
1）求数组元素中的素数之和；
2）对数组各元素进行排序（升序）。
由键盘输入6个整数存入二维数组（2行3列），打印当前数组，在主程序中调用这两个函数，分别输出：此数组元素中的素数之和；对数组各元素进行排序（升序）。
例如：
输入：2 3 5 9 8 7
输出：
Output matrix: 
2 3 5 
9 8 7
Prime number sum: 17
Sort: 2 3 5 7 8 9
*/