#include<stdio.h>
int main()
{
    int n,i,j,cont=0;
    scanf("%d",&n);
    for(i=1;i<n;i++)
    {
        for(j=2;j<i;j++)
        {
            if(i%j==0) break;
        }
        if(i==j)
        {
            cont++;
            printf("%-5d",j);
            if(cont%5==0) printf("\n");
        }
    }
    return 0;
}