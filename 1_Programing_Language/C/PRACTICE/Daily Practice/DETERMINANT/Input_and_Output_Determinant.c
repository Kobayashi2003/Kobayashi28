#include<stdio.h>
void Input(int str[][10],int n)
{
    for(int r=0;r<n;r++)
        for(int c=0;c<n;c++)
            scanf("%d",&str[r][c]);
}
void Output(int str[][10],int n)
{
    for(int r=0;r<n;r++)
    {
        for(int c=0;c<n;c++)
            printf("%d ",str[r][c]);
        putchar('\n');
    }
}
int main()
{
    int n,str[10][10]={0};
    scanf("%d",&n);
    
    Input(str,n);

    Output(str,n);

    return 0;
}