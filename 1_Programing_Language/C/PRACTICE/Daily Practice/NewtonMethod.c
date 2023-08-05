#include<stdio.h>
#include<math.h>
double NewtonModel(double num)//利用牛顿迭代法求一个数的平方根 公式：x_(n+1)=(x_n+a/x_n)/2
{
    double x=1;
    for(int i=1;i<=10;i++)
        x=(x+num/x)/2;
    return x;
}
int main()
{
    double num,sqrt;
    scanf("%lf",&num);
    printf("The square root of the num %-.3f is %-.3f\n",num,sqrt=NewtonModel(num));
    return 0;
}
