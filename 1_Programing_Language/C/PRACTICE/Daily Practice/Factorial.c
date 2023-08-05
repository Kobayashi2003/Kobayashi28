#include<stdio.h>
int main()
{
    int fac(int i);
    int n,factorial;
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
        factorial=fac(i);
    printf("%d\n",factorial);
    return 0;
}
int fac(int i)
{
    static int temp=1;
    temp=temp*i;
    return temp;
}