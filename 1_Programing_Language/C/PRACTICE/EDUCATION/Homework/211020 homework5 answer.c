#include<stdio.h>
int main()
{
    int i,t,n;
    scanf("%d",n);
    t=1;
    i=1;
    while(i<=n)
    {
        t=t*i;
        i=i+2;
    }
    printf("%d",t);
    return 0;
}
