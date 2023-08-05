#include <cstdio>
#include <cstring>
#include <algorithm>
#include <iostream>
using namespace std;
const int maxn = 100;
const int INF = 0x3f3f3f3f;
int p[maxn]; // 储存父节点
int edge[maxn][maxn]; // 邻接矩阵
int d[maxn]; // 到生成树的最短距离
int vis[maxn]; // 是否加入集合中
int n, m; // n 表示节点数， m 表示边的数目

//初始化
void init()
{
	memset(vis, 0, sizeof(vis)); // 集合为空(0)
	memset(p, -1, sizeof(p)); // 父节点为空(-1)
	for(int i=1;i<=n;i++) // 初始化邻接矩阵(对角为 1，其余无穷)
		for (int j = 1; j <= n; j++)
			i == j ? edge[i][j] == 0 : edge[i][j] = INF;
}

int prim()
{
	//以 1 作为根节点，找到所有和 1 连接的节点
	for (int i = 1; i <= n; i++)
	{
		d[i] = edge[1][i];
		p[i] = 1;
	}
	while (1)
	{
		int maxx = INF;		// 记录到生成树的最小距离
		int u = -1;      	// 记录到生成树的最小距离的节点编号

		//找到距离生成树最短距离的节点
		for (int i = 1; i <= n; ++i) {
			if (vis[i] == 0 && maxx > d[i]) {
				maxx = d[i];
				u = i;
			}
		}
		
		if (u == -1) // 不存在节点 i，说明树已完全生成，结束循环
			break;
		//将选出的节点纳入集合
		vis[u] = 1;

		//更新该节点影响的节点
		for (int i = 1; i <= n; ++i) {
			if (vis[i] == 0 && d[i] > edge[u][i]) {
				d[i] = edge[u][i];
				p[i] = u;
			}
		}
	}

	int sum = 0;
	 // 计算最小生成树的长度;
	for (int i = 1; i <= n; i++)
		sum += edge[i][p[i]];
	return sum;
}

int main()
{
	cin >> n;
	cin >> m;
	init(); 
	for (int i = 1; i <= m; i++)
	{
		int x, y, sp;
		cin >> x >> y >> sp;
		edge[x][y] = edge[y][x] = sp;
	}
	cout << prim() << endl;
	return 0;
}