#include<stdio.h>
void Input(int matrix[][10],int N,int M)
{
    for(int r=0;r<N;r++)//运用循环结构对二维数组内的元素进行赋值
    {
        printf("Plese input the  numbers of the %d row:\n",r+1);
        for(int c=0;c<M;c++)
            scanf("%d",&matrix[r][c]);
    }
}
void Saddle_Point(int matrix[][10],int N,int M)
{
    int count=0;
    for(int r=0;r<N;r++)
        for(int c=0;c<M;c++)
        {
            int temp=0;//定义temp用于判断r行c列的数是否符合条件
            for(int i=0;i<N;i++)
                if(matrix[r][c]>matrix[i][c])temp++;
            for(int j=0;j<M;j++)
                if(matrix[r][c]<matrix[r][j])temp++;
            if(temp==0)printf("the %d saddle is on the %d row and the %d colume,the number is: %d\n",++count,r+1,c+1,matrix[r][c]);
        } 
    if(count==0)printf("There is no saddle in this matrix\n");
}
int main()
{
    int matrix[10][10],N,M;
    printf("Please input the number of rows:\n");
    scanf("%d",&N);
    printf("Please input the number of columns:\n");
    scanf("%d",&M);
    Input(matrix,N,M);
    Saddle_Point(matrix,N,M);
    return 0;
}