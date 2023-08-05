#include<stdio.h>
void Input(int matrix[][10],int r,int c)
{
    for(int i=0;i<r;i++)
        for(int j=0;j<c;j++)
            scanf("%d",&matrix[i][j]);
}
void Output(int matrix[][10],int r,int c)
{
    for(int i=0;i<r;i++,putchar('\n'))
        for(int j=0;j<c;j++,putchar(' '))
            printf("%d",matrix[i][j]);        
}
int main()
{
    int matrix[10][10],r,c;
    scanf("%d %d",&r,&c);
    Input(matrix,r,c);
    Output(matrix,r,c);
    return 0;
}