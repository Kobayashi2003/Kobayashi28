#include <stdio.h>

int a[100][100] = { 0 };

int main()
{
	int n, m;                //矩阵的行数、列数
	int max, min;
	int i, j, k;
	int cnt = 0;
	int row = 0, col = 0;    //鞍点的行 列 
	scanf("%d %d", &n, &m);
	for (i = 0; i < n; i++)
	{
		for (j = 0; j < m; j++)
		{
			scanf("%d", &a[i][j]);
		}
	}

	//寻找鞍点
	for (i = 0; i < n; i++)
	{
		max = a[i][0];
		for (j = 0; j < m; j++)
		{
			if (a[i][j] > max)
			{
				max = a[i][j];
				col = j;
			}
		}
		min = a[0][col];
		for (k = 0; k < n; k++)
		{
			if (a[k][col] < min)
			{
				min = a[k][col];
				row = k;
			}
		}
		// 当前行的最大值 和 当前列的最小值 
		if (min == max)
		{
			cnt = 0;
			// 判断鞍点值行唯一
			for (k = 0; k < m; k++)
			{
				if (a[row][k] == max)
				{
					cnt++;
				}
			}
			if (cnt > 1)
			{
				printf("It does not exist");
				return 0;
			}
			cnt = 0;
			// 判断鞍点值列唯一
			for (k = 0; k < n; k++)
			{
				if (a[k][col] == max)
				{
					cnt++;
				}
			}
			if (cnt > 1)
			{
				printf("It does not exist");
				return 0;
			}
			// 行唯一&&列唯一；输出鞍点
			printf("a[%d][%d] = %d", row, col, a[row][col]);
			break;
		}
	}
	//找不到鞍点 输出NO 
	if (min != max)
	{
		printf("It does not exist");
	}
	return 0;
}


/*
测试样例1
4 5
1 2 3 5 4
2 4 6 8 10
3 6 9 12 15
4 8 12 16 20

测试样例2
4 5
1 2 3 12 4
2 4 6 8 10
3 6 9 12 15
4 8 12 16 20

测试样例3
3 3
1 3 3
4 5 6
7 8 9

测试样例4
3 3
1 2 5
2 5 5
7 8 9
*/