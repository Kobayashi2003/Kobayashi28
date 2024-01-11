#include<iostream>
#include<string.h>
using namespace std;
int n,m,a[20][20],h[20][20],ans;
//n,m表示行列，h数组表示是否取过 
void dfs(int x,int y,int he){
    ans=max(ans,he);//更新答案 
    int ty=y+1,tx=x;
    if(ty>m){
        tx=x+1;
        ty=1;
        if(tx>n)return;
    }//以上程序表示求出a[x][y]之后的下一个点 
    if(!h[tx][ty+1]&&!h[tx][ty-1]&&!h[tx+1][ty]&&!h[tx+1][ty+1]
    &&!h[tx+1][ty-1]&&!h[tx-1][ty]&&!h[tx-1][ty+1]&&!h[tx-1][ty-1]){
        //搜索八个方向，判断是否能取 
        h[tx][ty]=1;//打上标记（取过） 
        dfs(tx,ty,he+a[tx][ty]);//把这个点去上再递归 
        h[tx][ty]=0;//打回标记（未取过） 
    }
    dfs(tx,ty,he);//直接递归（表示这个点不取） 
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    cin>>n>>m;
    for(int ii=1;ii<=n;ii++){
            for(int jj=1;jj<=m;jj++){
                cin>>a[ii][jj];//输入 
            }
    }
    h[1][1]=1;
    dfs(1,1,a[1][1]);//假设第一个点取了 
    memset(h,0,sizeof(h));
    dfs(1,1,0);//假设第一个没有取
    memset(h,0,sizeof(h));

    cout<<ans;
    ans=0;
    
    return 0;
}