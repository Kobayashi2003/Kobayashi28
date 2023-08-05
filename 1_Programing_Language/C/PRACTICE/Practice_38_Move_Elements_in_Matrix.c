#include<stdio.h>
#define N 3
void change(int *p1,int *p2)//定义空函数change用于交换两指针所指向的元素
{
    int tmp=*p1;
    *p1=*p2;
    *p2=tmp;
}
void Move(int *head,int **flg)
{
    int *p[5]={head},*find,i,j,cont;
    for(find=head;find<head+N*N;find++)//找出最大值
        if(*p[0]<*find) p[0]=find;
    p[1]=p[2]=p[3]=p[4]=p[0];
    for(find=head;find<head+N*N;find++)//插入排序 找出4个最小值
    {
        cont=0;
        for(i=1;i<5&&*find>*p[i];i++,cont++);
        for(i=4;i>cont+1;i--)p[i]=p[i-1];
        p[cont+1]=find; 
    }
    for(i=0;i<5;i++) //交换
    {
        change(p[i],flg[i]);
        for(j=0;j<5;j++)
            if(p[j]==flg[i])p[j]=p[i];
    }
}
int main()
{
    int matrix[N][N];
    int i,j,*flg[]={&matrix[N/2][N/2],&matrix[0][0],&matrix[0][N-1],&matrix[N-1][0],&matrix[N-1][N-1]};
    for(i=0;i<N;i++)
        for(j=0;j<N;j++)
            scanf("%d",&matrix[i][j]);
    Move(*matrix,flg);
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
            printf("%4d",matrix[i][j]);
        putchar('\n');
    }
    return 0;
}