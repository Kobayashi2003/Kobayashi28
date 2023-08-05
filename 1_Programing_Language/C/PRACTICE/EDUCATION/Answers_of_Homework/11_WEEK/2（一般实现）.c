#include<stdio.h>

int main()
{
	int a, b, c, d, t;
	printf("请输入四个数(输入以空格分隔）：");
	scanf("%d %d %d %d", &a, &b, &c, &d);
	if (a < b)
	{
		t = a;
		a = b;
		b = t;           //利用中间变量t达到交换目的
	}
	if (a < c)
	{
		t = a;
		a = c;
		c = t;
	}
	if (a < d)
	{
		t = a;
		a = d;
		d = t;
	}
	if (b < c)
	{
		t = b;
		b = c;
		c = t;
	}
	if (b < d)
	{
		t = b;
		b = d;
		d = t;
	}
	if (c < d)
	{
		t = c;
		c = d;
		d = t;
	}
	printf("从大到小的顺序为 %d %d %d %d\n", a, b, c, d);
	return 0;
}