#include<stdio.h>
#define N 3
int main()
{
    int matrix[N][N],i,j,*flg,tmp;
    for(i=0;i<N;i++)
        for(j=0;j<N;j++) 
            scanf("%d",&matrix[i][j]);
    for(i=0;i<N;i++)
    {
        flg=&matrix[i][0];
        for(j=0;j<N;j++)
        {
            if(*flg<matrix[i][j])
            {
                flg=&matrix[i][j];
            }
        }
        tmp=matrix[i][i];
        matrix[i][i]=*flg;
        *flg=tmp;
    }
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
            printf("%3d",matrix[i][j]);
        printf("\n");
    }
    return 0;
}