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

	printf("\nѧ��       ����   �ɼ�1   �ɼ�2  �ɼ�3    ƽ���ɼ�\n");
	for (i = 0; i < N; i++)
	{
		printf("%5s%10s", stu[i].id, stu[i].name);
		for (j = 0; j < 3; j++)
			printf("%7d", stu[i].score[j]);
		printf("    %8.2f\n", stu[i].ave);
	}
	printf("�ܵ�ƽ���ɼ�Ϊ��%5.2f\n", average_score);
	printf("��߷�ѧ����ѧ�ţ�%s��������%s\n", stu[maxi].id, stu[maxi].name);
	printf("��ɼ��ֱ�Ϊ��%6d,%6d,%6d,ƽ���ɼ���%5.2f.\n",
		stu[maxi].score[0], stu[maxi].score[1], stu[maxi].score[2], stu[maxi].ave);
	return 0;
}

void input(struct student stu[])
{
	int i, j;
	for (i = 0; i < N; i++)
	{
		printf("\n�����%d��ѧ�������ݣ�\n", i + 1);
		printf("ѧ�ţ�");
		scanf("%s", stu[i].id);
		printf("������");
		scanf("%s", stu[i].name);
		for (j = 0; j < 3; j++)
		{
			printf("��%d�ſγɼ���", j + 1);
			scanf("%d", &stu[i].score[j]);
		}
		printf("\n");
	}
}

/*
21001 James 60 60 60
21002 ���� 70 70 70
21003 ���� 80 80 80
21004 John 90 90 90
21005 ���� 100 100 100
*/
