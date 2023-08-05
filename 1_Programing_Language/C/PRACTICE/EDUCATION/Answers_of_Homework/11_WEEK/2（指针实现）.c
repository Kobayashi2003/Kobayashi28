#include<stdio.h>

void swap(int* a, int* b);

int main()
{
	int a, b, c, d;
	printf("请输入四个数(输入以空格分隔）：");
	scanf("%d %d %d %d", &a, &b, &c, &d);
	if (a < b)
	{
		swap(&a, &b);
	}
	if (a < c)
	{
		swap(&a, &c);
	}
	if (a < d)
	{
		swap(&a, &d);
	}
	if (b < c)
	{
		swap(&b, &c);
	}
	if (b < d)
	{
		swap(&b, &d);
	}
	if (c < d)
	{
		swap(&c, &d);
	}
	printf("从大到小的顺序为 %d %d %d %d\n", a, b, c, d);
	return 0;
}

// 交换函数
void swap(int* a, int* b)
{
	int temp = *a;
	*a = *b;
	*b = temp;
}