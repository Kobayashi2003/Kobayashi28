#include<stdio.h>
#include<math.h>
int main() 
{
    int s_n=0,n,num,elements=0;
    printf("please input the number and the time:\n");
    scanf("%d %d",&num,&n);
    for(int i=1;i<=n;i++)
    {
        for(int j=1;j<=i;j++)
            elements+=num*pow(10,j-1);
    s_n+=elements;
    elements=0;
    }
    printf("%d",s_n);
    return 0;
}