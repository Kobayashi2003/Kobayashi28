#include<stdio.h>
int power(int num,int n)
{
    return n==0?1:num*power(num,n-1);
}
int main()
{
    int num,n;
    scanf("%d%d",&num,&n);
    printf("%d",power(num,n));
    return 0;
}