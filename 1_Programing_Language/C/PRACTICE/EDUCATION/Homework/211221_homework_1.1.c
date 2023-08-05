#include<stdio.h>
int main()
{
    void inv(int x[],int n);
    int i,a[10]={3,7,9,11,0,6,75,4,2};
    printf("The original array:\n");
    for(i=0;i<10;i++)
        printf("%d ",a[i]);
    printf("\n");
    inv(a,10);
    printf("The arrauhas been iverted:\n");
    for(i=0;i<10;i++)
        printf("%d ",a[i]);
    printf("\n");
    return 0;
}
void inv(int x[],int n)
{
    int temp,i,j,m=(n-1)/2;
    for(i=0;i<=m;i++)
    {
        j=n-i-1;
        temp=x[i];x[i]=x[j];x[j]=temp;
    }
    return;
}