#include<stdio.h>
int fac(int num)
{
    if(num==0) return 1;
    return num*fac(num-1);
}
int main()
{
    int n;
    long double E=0.0;
    scanf("%d",&n);
    while(n)
    {
        E+=1/(long double)fac(n--);
        printf("%.10Lf\n",E+1);
    }
    return 0;
}
//12的拟合度较高