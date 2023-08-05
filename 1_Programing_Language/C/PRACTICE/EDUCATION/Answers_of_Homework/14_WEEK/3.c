#include <stdio.h>

#define MAXN 1010
int a[MAXN];

int main()
{
	int n;
	int i, j, h;
	int ans, s;
	scanf("%d", &n);
	for (i = 0; i < n; i++)
	{
		scanf("%d", &a[i]);
	}
	ans = -1;
	for (i = 0; i < n; i++)
	{
		h = a[i];
		for (j = i; j < n; j++)
		{
			if (a[j] < h)
				h = a[j];
			s = (j - i + 1) * h;
			if (ans < s)
				ans = s;
		}
	}
	printf("%d\n", ans);
	return 0;
}

/*
测试样例1
6
3 1 6 5 2 3

测试样例2
5
1 2 3 4 5

测试样例3
5
4 2 3 4 4
*/