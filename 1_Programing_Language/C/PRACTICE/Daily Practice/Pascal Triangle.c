#include<stdio.h>
int main()
{
    int n,tri[100][100]={{1}};
    scanf("%d",&n);
    for(int r=1;r<n;r++)
    {
        tri[r][0]=1;
        for(int c=1;c<=r;c++)
            tri[r][c]=tri[r-1][c]+tri[r-1][c-1];
    }
    for(int r=0;r<n;r++)
    {
        for(int c=0;c<=r;c++)
            printf("%d ",tri[r][c]);
        putchar('\n');
    }
    return 0;
}