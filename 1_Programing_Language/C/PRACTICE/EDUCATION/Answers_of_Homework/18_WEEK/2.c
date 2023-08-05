#include <stdio.h>
struct Date
{
	int year;
	int month;
	int day;
};

int days(struct Date date);

int main()
{
	int day_sum;
	struct Date date;
	printf("input year month day:\n");
	scanf("%d %d %d", &date.year, &date.month, &date.day);
	day_sum = days(date);
	printf("%d/%d is the %dth day in %d ", date.month, date.day, day_sum, date.year);
	switch(day_sum%7){
		case 0: 
			printf("and it is Monday.\n");
			break;
		case 1: 
			printf("and it is Tuesday.\n");
			break;
		case 2: 
			printf("and it is Wednesday.\n");
			break;
		case 3: 
			printf("and it is Thursday.\n");
			break;
		case 4: 
			printf("and it is Friday.\n");
			break;
		case 5: 
			printf("and it is Saturday.\n");
			break;
		case 6: 
			printf("and it is Sunday.\n");
			break;
	}
	return 0; 
}

int days(struct Date date)
{
	int day_sum, i;
	int day_tab[] = { -1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
	day_sum = 0;
	for (i = 1; i < date.month; i++)
		day_sum += day_tab[i];
	day_sum += date.day;
	if (((date.year % 4 == 0 && date.year % 100 != 0) || date.year % 400 == 0) && date.month >= 3)
		day_sum += 1;
	return day_sum;
}

/*
测试样例：2000 3 1
输出：3/1 is the 61th day in 2000 and it is Saturday.

样例2：1900 3 1
输出：3/1 is the 60th day in 1900 and it is Friday.

样例3：2000 1 1
输出：1/1 is the 1th day in 2000 and it is Tuesday. 
*/ 
