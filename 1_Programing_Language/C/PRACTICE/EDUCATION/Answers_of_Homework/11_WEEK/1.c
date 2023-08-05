#include<stdio.h>

int main()
{
	int score, temp;
	char ret;
	printf("请输入成绩：\n");		//提示语
	scanf("%d", &score);
	temp = score / 10;		        //求出成绩的十位数
	switch(temp)
	{
		case 10:
		case 9:
			ret = 'A';
			break;
		case 8:
			ret = 'B';
			break;
		case 7:
			ret = 'C';
			break;
		case 6:
			ret = 'D';
			break;
		case 5:
		case 4:
		case 3:
		case 2:
		case 1:
		case 0:
			ret = 'E';
			break;
		default:
			break;
	}
	printf("成绩等级为：%c\n", ret);
	return 0;
}