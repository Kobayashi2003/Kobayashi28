#include<stdio.h>
#define N 5
#define Mark 2
#define Queen 'Q'
int MemeryTable[N]={0};
int Flag[N][N]={0};
int Flag_Save[N]={0};

void Save(int (*Flag_temp)[N])
{
    for(int i=0;i<N;i++)
        Flag_Save[i]=Flag_temp[0][i];
}

int Stop(int (*Flag)[N])
{
    int count=0;
    for(int i=0;i<N;i++)if(Flag[0][i]==Flag_Save[i])count++;
    if(count==N)return 1;
    return 0;
}

void Output(int (*matrix)[N])
{
    for(int i=0;i<N;i++,putchar('\n'))
        for(int j=0;j<N;j++)
        {
            if(matrix[i][j]=='Q')printf("Q ");
            else printf(". ");
        }
    putchar('\n');
}

void makeMark(int (*matrix)[N],int x,int y)
{
    const int dx[]={-1,-1,-1,0,0,1,1,1};//方位
    const int dy[]={1,0,-1,1,-1,1,0,-1};
    for(int distance=1;distance<N;distance++)//距离
        for(int i=0;i<8;i++)
        {
            int nx=x+distance*dx[i];
            int ny=y+distance*dy[i];
            if(nx>=0&&ny>=0&&nx<N&&ny<N) matrix[nx][ny]+=Mark;
        }
}

void cleanMark(int (*matrix)[N],int x,int y)
{
    const int dx[]={-1,-1,-1,0,0,1,1,1};
    const int dy[]={1,0,-1,1,-1,1,0,-1};
    for(int distance=0;distance<N;distance++)
        for(int i=0;i<8;i++)
        {
            int nx=x+distance*dx[i];
            int ny=y+distance*dy[i];
            if(nx>=0&&ny>=0&&nx<N&&ny<N) matrix[nx][ny]-=Mark;
        }
    matrix[x][y]=0;
}

void placeQueens(int (*board)[N],int r)//按行进行摆放 r表示为行
{
    static int count=0,sign=0;
    int On_Off=0;
    
    if(r<N)
    {
        for(int c=0;c<N;c++)//放置在该行的哪一位置,既哪一列  
        {
            if(board[r][c]==0&&Flag[r][c]==0)
            {
                board[r][c]=Queen;
                makeMark(board,r,c);
                Flag[r][c]='Q';
                MemeryTable[r]=c;
                On_Off++;
                break;
            }
        }
        switch(On_Off)
        {
            case 1:
            placeQueens(board,r+1);
            break;
            case 0:
            cleanMark(board,r-1,MemeryTable[r-1]);
            for(int c=0;c<N;c++) Flag[r][c]=0;
            
            placeQueens(board,r-1);
            break;
        }
    }

    if(Flag[0][N-1]!=0)sign=1;
    if(Stop(Flag)!=0&&sign==1)return;

    if(r==N-1)
    {
        count++;
        if(count==1)Save(Flag);
        printf("the %d answer is:\n",count);
        Output(board);
        cleanMark(board,r,MemeryTable[r]);
        Flag[r][MemeryTable[r]]='Q';
        placeQueens(board,r);
    }
}

int main()
{
    int board[N][N]={0};
    placeQueens(board,0);
    return 0;
}