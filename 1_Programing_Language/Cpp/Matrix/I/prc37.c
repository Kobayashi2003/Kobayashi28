#include <stdio.h>

#define N_stu 2
#define N_sub 3

void avg(double *p) {
    int n = N_stu * N_sub;
    double sum = 0;
    for (int i = 0; i < n; ++i)
        sum += p[i];
    printf("%.2lf\n", sum / n);
}

void avg_i(double (*p)[N_sub], int ID) {
    double sum = 0;
    for (int i = 0; i < N_sub; ++i)
        sum += p[ID][i];
    printf("%.2lf\n", sum / N_sub);
}

int main()
{
	int i, j;
	double score[N_stu][N_sub];

	for (i = 0; i < N_stu; i++)
	{
		for (j = 0; j < N_sub; j++)
		{
			scanf("%lf", &score[i][j]);
		}
	}

	double *p = score[0];
	double (*p_i)[N_sub] = score;

	//goal function
	avg(p); 
	avg_i(p_i, 0);
	avg_i(p_i, 1);

	return 0;
}
