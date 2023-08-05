#include <stdio.h>

int fun1(int m, int n);
int fun2(int m, int n, int p);

int main()
{
	int n, m, p, q, t;
	scanf("%d %d", &m, &n);
	if (m < n)   // 使得m为较大值，n为较小值
	{
		t = m;
		m = n;
		n = t;
	}
	p = fun1(m, n);
	q = fun2(m, n, p);
	printf("最大公约数为：%d\n最小公倍数为：%d\n", p, q);
	return 0;
}

int fun1(int m, int n)
{
	int tmp;			//余数，当余数为0的时候，最后的m即为最大公约数
	//先用较小的数对较大的数取余，再用余数对较小的数求余，直到余数为零 
	while (n > 0)
	{
		tmp = m % n;
		m = n;
		n = tmp;
	}
	return m;
}

int fun2(int m, int n, int p)
{
	return m * n / p;
}

/*
测试样例1
8 6

测试样例2
6 8
*/