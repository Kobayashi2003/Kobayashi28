#include<stdio.h>
void Input(int matrix[][10],int r,int c)
{
    for(int i=0;i<r;i++)
    {
        printf("Please int put the elements of the %d row:\n",i+1);
        for(int j=0;j<c;j++)
            scanf("%d",&matrix[i][j]);
    }
}
void Output(int matrix[][10],int r,int c)
{
    for(int i=0;i<r;i++,putchar('\n'))
        for(int j=0;j<c;j++,putchar(' '))
            printf("%d",matrix[i][j]);        
}
void Multiplication(int matrix_1[][10],int matrix_2[][10],int r1,int c1,int r2,int c2)
{
    int matrix_mul[10][10];
    for(int r=0;r<r1;r++)
        for(int c=0;c<c2;c++)
            for(int i=0;i<c1;i++)
                matrix_mul[r][c]+=matrix_1[r][i]*matrix_2[i][c];
    Output(matrix_mul,r1,c2);
}
int main()
{
    int matrix_1[10][10],matrix_2[10][10],r1,c1,r2,c2;
    printf("Please input the number of rows and columns of the first matrix:\n");
    scanf("%d %d",&r1,&c1);
    printf("Please input the elements of the first matrix\n\n");
    Input(matrix_1,r1,c1);
    printf("Please input the number of rows and columns of the second matrix:\n");
    scanf("%d %d",&r2,&c2);
    printf("Please input the elements of the second matrix\n\n");
    Input(matrix_2,r2,c2);
    Multiplication(matrix_1,matrix_2,r1,c1,r2,c2);
    return 0;
}