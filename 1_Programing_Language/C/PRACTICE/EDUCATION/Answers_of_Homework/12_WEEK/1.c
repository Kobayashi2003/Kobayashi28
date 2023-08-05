#include<stdio.h>
int main()
{
	char c;
	int letters = 0;
	int space = 0;
	int digit = 0;
	int others = 0;
	printf("请输入一行字符：\n");
	while ((c = getchar()) != '\n')
	{
		if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
		{
			letters++;
		}
		else if (c == ' ')
		{
			space++;
		}
		else if (c >= '0' && c <= '9')
		{
			digit++;
		}
		else
		{
			others++;
		}
	}
	printf("英文字母%d个，空格%d个，数字%d个，其他字符%d个\n", letters, space, digit, others);
	return 0;
}
