#include<stdio.h>
#define N 8
const int dx[]={-1,1,0,0,-1,-1,1,1};
const int dy[]={0,0,-1,1,-1,1,-1,1};
int main()
{
    int matrix[N][N]={0};
    int x=3,y=2;
    matrix[x][y]=9;
    for(int i=1;i<N;i++)
    {
        for(int j=0;j<8;j++) 
        {
            int nx=x+i*dx[j];
            int ny=y+i*dy[j];
            if(nx>=0&&nx<N&&ny>=0&&ny<N)matrix[nx][ny]=1;
        }
    }
    for(int i=0;i<N;i++,putchar('\n'))
        for(int j=0;j<N;j++)
            printf("%3d",matrix[i][j]);

    return 0;
}
