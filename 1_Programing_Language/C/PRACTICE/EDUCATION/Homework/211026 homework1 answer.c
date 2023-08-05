//问：我在没有ASCII表的时候能不能写出这个程序
#include <stdio.h>
int main()
{
	char in_c, out_c, base;
	int off = 4;
	scanf("%c", &in_c);
	if (in_c >= 'A' && in_c <= 'Z')
	{
		base = 'A';
	}
	else if (in_c >= 'a' && in_c <= 'z')
	{
		base = 'a';
	}
	out_c = ((in_c - base + off) % 26) + base;
	printf("%c\n", out_c);
	return 0;
}
