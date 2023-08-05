#include<stdio.h>
#define N 5
void change(int *p1,int *p2)//定义空函数change，用于交换两整型指针中的内容
{
    int temp;
    temp=*p1;
    *p1=*p2;
    *p2=temp;
}
void Sort(int *head,int *p_max,int *p_min1,int *p_min2,int *p_min3,int *p_min4)//定义空函数Sort
{
    int *find,*find_;
    //找出矩阵中的四个最小值，并将它们先按顺序暂存至矩阵的前四位中
    for(find=head;find<head+4;find++)
        for(find_=find;find_<head+N*N;find_++)
            if(*find_<*(find))change(find_,find);
    //将四个最小值放置在矩阵的四个对角
    change(p_min1,head);
    change(p_min2,head+1);
    change(p_min3,head+2);
    change(p_min4,head+3);
    //找出矩阵中的最大值，并将其放置在矩阵的中间
    for(find=head;find<head+N*N;find++)
        if(*find>*p_max)change(p_max,find);
}
int main()
{
    int matrix[N][N];
    int r,c;
    for(r=0;r<N;r++)
    {
        printf("Please enter the %d row:\n",r+1);
        for(c=0;c<N;c++)
            scanf("%d",&matrix[r][c]);
    }
    //用指针表示出矩阵的四顶点及中心的地址
    int *p_Max=&matrix[2][2],*p_Min1=&matrix[0][0],*p_Min2=&matrix[0][4],*p_Min3=&matrix[4][0],*p_Min4=&matrix[4][4];
    Sort(*matrix,p_Max,p_Min1,p_Min2,p_Min3,p_Min4);
    //输出矩阵
    for(r=0;r<N;r++)
    {
        for(c=0;c<N;c++)
            printf("%3d",matrix[r][c]);
        putchar('\n');
    }
    return 0;
}