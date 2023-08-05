#include<stdio.h>
#define MAXN 1010
int a[MAXN];
int main()
{
	int n, k;
	int i, j;
	for (i = 0; i < MAXN; i++)
	{
		a[i] = 0;
	}
	scanf("%d %d", &n, &k);
	for (i = 1; i <= k; i++)
	{
		for (j = 1; j <= n; j++)
		{
			if (j % i == 0)
			{
				a[j] = !a[j];
			}
		}
	}
	for (i = 1; i <= n; i++)
	{
		if (a[i])
		{
			printf("%d ", i);
		}
	}
	printf("\n");
	return 0;
}
