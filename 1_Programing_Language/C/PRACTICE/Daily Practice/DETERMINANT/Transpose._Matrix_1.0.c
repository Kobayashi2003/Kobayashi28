#include<stdio.h>
void Input(int matrix[][10],int n)
{
    for(int r=0;r<n;r++)
        for(int c=0;c<n;c++)
            scanf("%d",&matrix[r][c]);
}
void Output(int matrix[][10],int n)
{
    putchar('\n');
    for(int r=0;r<n;r++)
    {
        for(int c=0;c<n;c++)
            printf("%d ",matrix[r][c]);
        putchar('\n');
    }
}
void Transpose(int matrix[][10],int n)
{
    int matrix_temp[10][10];
    for(int r=0;r<n;r++) 
        for(int c=0;c<n;c++)
            matrix_temp[r][c]=matrix[c][r];
    for(int r=0;r<n;r++) 
        for(int c=0;c<n;c++)
            matrix[r][c]=matrix_temp[r][c];
}
int main()
{
    int matrix[10][10],n;
    scanf("%d",&n);
    Input(matrix,n);
    Transpose(matrix,n);
    Output(matrix,n);
    return 0;
}