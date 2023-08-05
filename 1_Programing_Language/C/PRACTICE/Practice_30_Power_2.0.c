#include<stdio.h>
#include<math.h>
int power(int num,int n)
{
    return n==0 ? 1 : (n%2==0 ? (int)pow((double)power(num,n/2),2.0) : num*power(num,n-1));
}
int main()
{
    int num,n;
    scanf("%d%d",&num,&n);
    printf("%d\n",power(num,n));
    return 0;
}