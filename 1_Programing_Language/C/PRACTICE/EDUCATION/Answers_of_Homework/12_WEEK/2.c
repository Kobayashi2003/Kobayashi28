#include<stdio.h>
int main()
{
	int i, j, k, n;
	scanf("%d", &n);
	for (i = n; i > 0; i--)
	{
		for (k = 0; k < n - i; k++)
		{
			printf(" ");
		}
		for (j = 0; j < 2 * i - 1; j++)
		{
			printf("#");
		}
		printf("\n");
	}
	return 0;
}
