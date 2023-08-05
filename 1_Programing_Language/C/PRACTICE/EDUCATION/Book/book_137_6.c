#include<stdio.h>
int main()
{
    int fac(int i);
    static int sum=0;
    int n;
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
        sum+=fac(i);
    printf("%d\n",sum);
    return 0;
}
int fac(int i)
{
    static int temp=1;
    temp*=i;
    return temp;
}