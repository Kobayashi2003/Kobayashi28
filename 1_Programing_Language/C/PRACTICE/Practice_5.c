//动态规划 硬币最轻问题
//n种不同面值的硬币
//面值分别为 Vi  重量分别为 Wi 
//且现要购买某种总币值为y的商品 那么应该如何选择付款方式使得付出钱币的总重量最轻
//使用动态规划设计策略设计一个求解该问题的算法

#include<stdio.h>
#define N 5
void solve(int *V,int *W,int n)
{
    
}
int main()
{
    int n;//首先得知道有多少种纸币
    scanf("%d",&n);
    int W[N]={0},V[N]={0};//然后需要知道每一种纸币的面值以及重量
    for(int i=0;i<n;i++)
    {
        printf("V%d=",i+1);
        scanf("%d",&V[i]);
        printf("W%d=",i+1);
        scanf("%d",&W[i]);
    }
    solve(V,W,n);//然后我们来开始对问题的求解
    return 0;
}