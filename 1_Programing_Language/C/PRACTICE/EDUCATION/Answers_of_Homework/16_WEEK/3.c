#include <stdio.h>
#include <string.h>

void swap(int *a, int *b)
{
	int temp = *a;
	*a = *b;
	*b = temp;
}

void transform(int *arr, int col_row)
{
	int i, j;
	//找到最大值
	int max = arr[0], max_idx;
	for (i = 0; i < col_row * col_row; i++)
	{
		if (max < arr[i]) //找出最大数
		{
			max = arr[i];
			max_idx = i;
		}
	}
	//行列相乘得到总数量，除以2后加1则为中心点（暂时不考虑偶数的情况）
	int center_idx = (col_row * col_row) / 2;
	swap(&arr[center_idx], &arr[max_idx]);

	//找到四个最小值
	int min_idx[4];
	for (i = 0; i < 4; i++) //循环4次获取到最小值
	{
		int min_tmp = arr[col_row * col_row - 1];
		for (j = 0; j < col_row * col_row; j++)   //遍历所有数据，逐个比较获取最小值
		{
			int k = 0;
			for (; k < i; k++)  //但是要注意如果某个下标的数据已经是获取过的最小值,则不能进行判断（因为这个肯定是最小的）
			{
				if (j == min_idx[k])
					break;
			}
			if (k != i)  //k和i不同表示j这个坐标已经是找到的最小的几个数字之一，则找下一个判断
			{
				continue;
			}
			if (min_tmp > arr[j])  // 相当于在剩下的数中找到最小的那个数字
			{
				min_tmp = arr[j];
				min_idx[i] = j; //并且记录这个数字的位置
			}
		}
	}
	int change_idx[4];//先计算四个角的下标，便于后边进行交换
	change_idx[0] = 0;//第一个要置换的数据的下标，也就是左上角
	change_idx[1] = col_row - 1;//第二个要置换的数据的下标，也就是右上角
	change_idx[2] = col_row * (col_row - 1);//第一个要置换的数据的下标，也就是左下角
	change_idx[3] = (col_row * col_row) - 1;//第一个要置换的数据的下标，也就是右下角
	for (i = 0; i < 4; i++)
	{
		swap(&arr[change_idx[i]], &arr[min_idx[i]]);
	}
	return;
}
int main()
{
	int arr[5][5];
	printf("Please enter a 5x5 matrix: \n");
	for (int i = 0; i < 5; i++)
	{
		for (int j = 0; j < 5; j++)
		{
			scanf("%d", &arr[i][j]);
		}
	}
	transform(*arr, 5);//将二维数组当做一维数组传入处理，并且传入行列数
	printf("\n");
	for (int i = 0; i < 5; i++)
	{
		for (int j = 0; j < 5; j++)
		{
			printf("%d ", arr[i][j]);
		}
		printf("\n");
	}
	return 0;
}

/*
输入样例1
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25

输入样例2
5 2 3 4 1
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
*/
