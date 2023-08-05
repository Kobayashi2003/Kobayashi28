#include<stdio.h>
int times(int n)
{
    int sum=0;
    for(int i=1;i<n;i++)
        sum+=i;
    return sum;
}
int Inversion_Number(int *str,int n)
{
    int inv=0;
    for(int i=1;i<=times(n);i++)
        for(int j=0;j<n-1;j++)
        {
            int temp;
            if(str[j]>str[j+1])
            {
                temp=str[j+1];
                str[j+1]=str[j];
                str[j]=temp;
                inv++;
            }
        }
    return inv;
}
int main()
{
    int n,inv,str[10]={1,2,3};
    scanf("%d",&n);
    inv=Inversion_Number(str,n);

    printf("%d\n",inv);
    return 0;
}