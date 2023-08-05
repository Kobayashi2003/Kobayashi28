#include <stdio.h>
#define N 5

struct student
{
	char id[6];
	char name[8];
	int score[3];
	float ave;
}stu[N];

void input(struct student stu[]);

int main()
{
	int i, j;
	float sum_score = 0, max_score = 0, average_score = 0;
	int maxi = 0;
	input(stu);
	for (i = 0; i < N; i++)
	{
		sum_score = 0;
		for (j = 0; j < 3; j++)
			sum_score += stu[i].score[j];
		stu[i].ave = sum_score / 3;
		average_score += stu[i].ave;
		if (sum_score > max_score)
		{
			max_score = sum_score;
			maxi = i;
		}
	}
	average_score /= N;

	printf("\n学号       姓名   成绩1   成绩2  成绩3    平均成绩\n");
	for (i = 0; i < N; i++)
	{
		printf("%5s%10s", stu[i].id, stu[i].name);
		for (j = 0; j < 3; j++)
			printf("%7d", stu[i].score[j]);
		printf("    %8.2f\n", stu[i].ave);
	}
	printf("总的平均成绩为：%5.2f\n", average_score);
	printf("最高分学生的学号：%s，姓名：%s\n", stu[maxi].id, stu[maxi].name);
	printf("其成绩分别为：%6d,%6d,%6d,平均成绩：%5.2f.\n",
		stu[maxi].score[0], stu[maxi].score[1], stu[maxi].score[2], stu[maxi].ave);
	return 0;
}

void input(struct student stu[])
{
	int i, j;
	for (i = 0; i < N; i++)
	{
		printf("\n输入第%d个学生的数据：\n", i + 1);
		printf("学号：");
		scanf("%s", stu[i].id);
		printf("姓名：");
		scanf("%s", stu[i].name);
		for (j = 0; j < 3; j++)
		{
			printf("第%d门课成绩：", j + 1);
			scanf("%d", &stu[i].score[j]);
		}
		printf("\n");
	}
}

/*
21001 James 60 60 60
21002 李四 70 70 70
21003 王五 80 80 80
21004 John 90 90 90
21005 张三 100 100 100
*/
