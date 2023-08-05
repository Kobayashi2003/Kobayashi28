#include<stdio.h>

int main()
{
	char str[50], *p = str;
	int i, k = 0, flag = 0, sum, a[100] = { 0 }, *q = a;
	gets(str);
	for (i = 0; *(p + i) != '\0'; i++)
	{
		if ((*(p + i) >= '0') && (*(p + i) <= '9'))
		{
			sum = k + 1;
			*(q + k) = (*(q + k)) * 10 + (*(p + i)) - '0';
			flag = 1;
		}
		else if (flag != 0)
		{
			k++;
			*(q + k) = 0;
			flag = 0;
		}
	}
	for (i = 0; i < sum; i++)
		printf("%d\n", *(q + i));
	printf("sum=%d\n", sum);
	return 0;
}

/*
输入样例
ab123a 456

*/