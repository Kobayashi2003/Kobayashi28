#include<stdio.h>

int main()
{
	int x, a, b, c, d, e;
	scanf("%d", &x);
	a = x / 10000;
	b = (x % 10000) / 1000;
	c = (x % 1000) / 100;
	d = (x % 100) / 10;
	e = x % 10;
	if (a != 0)
	{
		printf("这是5位数\n");
		printf("每位数字：%d %d %d %d %d\n", a, b, c, d, e);
		printf("逆序为：%d%d%d%d%d\n", e, d, c, b, a);
	}
	else if (b != 0)
	{
		printf("这是四位数\n");
		printf("每位数字：%d %d %d %d\n", b, c, d, e);
		printf("逆序为：%d%d%d%d\n", e, d, c, b);
	}
	else if (c != 0)
	{
		printf("这是三位数\n");
		printf("每位数字：%d %d %d\n", c, d, e);
		printf("逆序为：%d%d%d\n", e, d, c);
	}
	else if (d != 0)
	{
		printf("这是两位数\n");
		printf("每位数字：%d %d\n", d, e);
		printf("逆序为：%d%d\n", e, d);
	}
	else if (e != 0)
	{
		printf("这是一位数\n");
		printf("每位数字：%d\n", e);
		printf("逆序为：%d\n", e);
	}
	return 0;
}
