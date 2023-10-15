#include <stdio.h>

#define M  60
#define N  3

void selectionSort (int *nu, int(*p)[N], int *tot, int size);

int swap(int *p, int *q);


void selectionSort (int * nu, int(*p)[N], int *tot, int size) {
    for (int i = 0; i < size; ++i) {
        int max = i;
        for (int j = i+1; j < size; ++j) {
            if (tot[j] > tot[max]) 
                max = j;
            if (tot[j] == tot[max] && nu[j] < nu[max])
                max = j;
        }
        if (max != i) {
            swap(&nu[i], &nu[max]);
            for (int k = 0; k < N; ++k) {
                swap(&p[i][k], &p[max][k]);
            }
            swap(&tot[i], &tot[max]);
        }
    }
}

int swap(int *p, int *q) {
    int tmp = *p;
    *p = *q;
    *q = tmp;
    return 0;
}


int input(int *nu, int(*p)[N], int *tot);
void print(const int *nu, const int(*p)[N], const int *tot, int size);

int main(void)
{
	int stuNumber = 0;
	int stuNum[M], grade[M][N], total[M] = {0};

	//input and total
	//printf("please input number(-1 for ends)");
	//printf("and math,english,computer grade:\n");
	stuNumber = input(stuNum, grade, total);

	if (stuNumber == 0)
		return 0;   

	printf("Original grades:\n");
	printf("stuNum   math       english    computer   total\n");
	print(stuNum, grade, total, stuNumber);
	printf("---------------------------------------------------\n");

	//selection sorting --- goal function
	selectionSort (stuNum, grade, total, stuNumber);

	//output sorting result
	printf("descending sort by total grades:\n");
	printf("stuNum    Math      English    Computer   Total\n");
	print(stuNum, grade, total, stuNumber);

	return 0;
}


int input(int *nu, int(*p)[N], int *tot)
{
	int i = 0, j = 0;
	int n, g[N];

	scanf("%d", &n);        
	for (j = 0; j < N; j++)
		scanf("%d", &g[j]);

	while (n != -1 && i < M)
	{
		*(nu + i) = n; 
		for (j = 0; j < N; j++)
		{
			*(*(p + i) + j) = g[j]; 
			*(tot + i) += g[j];
		}

		i++;

		scanf("%d", &n);    
		for (j = 0; j < N; j++)
			scanf("%d", &g[j]);
	}
	return i;
}


void print(const int *nu, const int(*p)[3], const int *tot, int size)
{
	int i, j;
	for (i = 0; i < size; i++)
	{
		printf("%-10d ", *(nu + i)); 
		for (j = 0; j < N; j++)
			printf("%-10d ", *(*(p + i) + j));
		printf("%-10d ", *(tot + i));
		printf("\n");
	}
}
