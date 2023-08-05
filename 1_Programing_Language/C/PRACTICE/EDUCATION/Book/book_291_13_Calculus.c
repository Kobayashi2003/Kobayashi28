#include<stdio.h>
#include<math.h>
#define Precision 1/1e6
//#include<time.h>
double fun1(double x)
{
    return sin(x);
}
double fun2(double x)
{
    return cos(x);
}
double fun3(double x)
{
    return exp(x);
}
void Calculus(double (*fun)(double x),double x1,double x2)
{
    double sum=0;
    for(;x1<x2;x1+=Precision)
    {
        sum+=(*fun)(x1)*Precision;
    }
    printf("The result is:%lf\n",sum);
}
int main()
{
    //clock_t t=clock();
    Calculus(fun1,0.0,1.0);
    Calculus(fun2,0.0,1.0);
    Calculus(fun3,0.0,1.0);
    //t-=clock();
    //printf("time:%fs\n",-((float)t)/CLOCKS_PER_SEC);
    return 0;
}