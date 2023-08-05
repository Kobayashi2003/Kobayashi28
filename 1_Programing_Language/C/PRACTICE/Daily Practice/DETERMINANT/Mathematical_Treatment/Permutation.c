#include<stdio.h>
void permutation(int a[],int n,int k)
{
    static int c[10]={0};
    if(k==0) 
        for(int i=0;i<n;i++) c[i]=a[i];
    int b[10]={0};
    for(int i=0;i<k;i++)
        b[i]=a[i];
    b[k]=c[k];

    if(k<n)
    {
        for(int i=0;i<=k;i++)
        {
            int temp=b[i];
            b[i]=b[k];
            b[k]=temp;
            permutation(b,n,k+1);
            temp=b[i];
            b[i]=b[k];
            b[k]=temp;
        }
    }
    if(k==n) 
    {
        for(int i=0;i<n;i++)
            printf("%d",b[i]); 
        printf("\n");
    }
}
int main()
{
    int a[]={1,2,3};
    int n=3;
    permutation(a,n,0);

    return 0;
}


