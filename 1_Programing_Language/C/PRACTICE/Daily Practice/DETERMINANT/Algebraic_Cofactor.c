#include<stdio.h>
#include<math.h>
void Input(int det[][10],int n)
{
    for(int r=0;r<n;r++)
        for(int c=0;c<n;c++)
            scanf("%d",&det[r][c]);
}
void Output(int det[][10],int n)
{
    for(int r=0;r<n;r++)
    {
        for(int c=0;c<n;c++)
            printf("%d ",det[r][c]);
        putchar('\n');
    }
    putchar('\n');
}
void Cofactor(int det[][10],int n,int i,int j)
{
    int Cof_i_j[10][10];
    for(int r=0,r_temp=0;r<n;r++,r_temp++)
    {
        if(r==i)r++;
        for(int c=0,c_temp=0;c<n;c++,c_temp++)
        {
            if(c==j)c++;
            Cof_i_j[r_temp][c_temp]=det[r][c];
        }
    }
    Output(Cof_i_j,n-1);
}
int main()
{
    int det[10][10],n,i,j;
    scanf("%d",&n);
    Input(det,n);
    Output(det,n);
    scanf("%d %d",&i,&j);
    Cofactor(det,n,i-1,j-1);
    return 0;
}