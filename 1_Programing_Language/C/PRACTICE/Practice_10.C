#include<stdio.h>
#define N 10
#define TURE 1
#define FALSE 0
int n,m,r,c,num;
int check(int (*matrix)[N],int n_tmp,int m_tmp)
{
    for(c=0;num>matrix[0][c]&&c<m_tmp;c++);
    if(num==matrix[0][c]&&c<m_tmp) return TURE;
    if(c-1>=0)
    {
        for(r=0;num>matrix[r][c-1]&&r<n_tmp;r++);
        if(num==matrix[r][c-1]&&r<n_tmp) return TURE;
        if(n_tmp>0&&m_tmp>0)
            return check(&matrix[r],n_tmp-r+1,c-1);
    }
    return FALSE;    
}
int main()
{
    int matrix[N][N]={0};
    scanf("%d%d",&n,&m);
    for(r=0;r<n;r++)
        for(c=0;c<m;c++)
            scanf("%d",&matrix[r][c]);
    scanf("%d",&num);
    printf("result:%s\n",(check(matrix,n,m)==1)?"TURE":"FALSE");
    return 0;
}
//在一个自左向右 自上而下递增的n*m矩阵中 判断一个数是否存在