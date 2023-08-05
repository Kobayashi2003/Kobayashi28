#include<stdio.h>
#define N 3
int main()
{
    int MagicSquare[N][N]={0},i=0,j=N/2;
    for(int num=1;num<=N*N;num++)
    {
        MagicSquare[i][j]=num;
        if(num%N!=0)
        {
            i=(i-1+N)%N;
            j=(j+1)%N;   
        }
        else i=(i+1)%N;
    }
    for(int r=0;r<N;r++,putchar('\n'))
        for(int c=0;c<N;c++)
            printf("%5d",MagicSquare[r][c]);
    return 0;
}