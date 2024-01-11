#include <iostream>
#define REG register

using namespace std;

typedef long long LL;

const int kN = 1e6 + 10;

int v[kN], l[kN], r[kN];
//v[i]:节点i权值，l[i]:编号为i的节点的左孩子的编号
//r[i]:编号为i的节点的右孩子的编号
int N, ans = 0;
bool pd; //判断是否为对称二叉子树

int cnt(int x) { //计算以x为根节点的对称二叉子树的节点数
  int sum = 0;
  if (l[x] != -1) sum += cnt(l[x]);
  if (r[x] != -1) sum += cnt(r[x]);
  return sum + 1; //别忘了根节点
}

void check(int x, int y) { //判断对称二叉子树
  if (x == -1 && y == -1) return ; //如果已经到底了，结束
  if (x == -1 || y == -1 || v[x] != v[y]) { //不对称
    pd = false; return ;
  }
  check(l[x], r[y]);
  check(r[x], l[y]); //这里代码后插图另作解释
}

int main() {
  scanf("%d", &N);
  for (REG int i = 1; i <= N; ++i)
    scanf("%d", &v[i]);
  for (REG int i = 1; i <= N; ++i)
    scanf("%d%d", &l[i], &r[i]);
  ans = 1; //至少有一个对称（一个节点）

  for (REG int i = 1; i <= N; ++i) { //枚举对称二叉子树的根节点
    if (l[i] != -1 && r[i] != -1 && v[l[i]] == v[r[i]]) {
      pd = true; //先默认为是对称二叉子树
      check(l[i], r[i]);
      if (pd) ans = max(ans, cnt(i)); //如果是对称二叉子树就可以计算节点数取最大值了
    }
  }
  printf("%d\n", ans);
  return 0;
}