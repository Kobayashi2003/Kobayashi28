#include <stdio.h>
#include <stdlib.h>


int checkPossibility(int *nums, int numsSize) {

    int flg1 = 1, flg2 = 1;
    for (int i = 0; i < numsSize-1; ++i) {
        int x = nums[i], y = nums[i+1];
        if (x > y) {
            nums[i] = y;
            for (int j = 0; j < numsSize-1; ++j) {
                if (nums[j] > nums[j + 1]) {
                    flg1 = 0;
                    break;
                }
            }

            nums[i] = x;
            nums[i + 1] = x;
            for (int j = 0; j < numsSize-1; ++j) {
                if (nums[j] > nums[j + 1]) {
                    flg2 = 0;
                    break;
                }
            }
            break;
        }
    }
    return flg1 || flg2;
}

int main()
{
	int N;
	scanf("%d", &N);

	int *arr;
	arr = (int *) malloc(N * sizeof(int));

	int i;
	for (i = 0; i < N; i++)
	{
		scanf("%d", &arr[i]);
	}

	int rst = -1;
	rst = checkPossibility(arr, N);		//goal function

	switch (rst)
	{
		case 0:
			printf("NO");
			break;
		case 1:
			printf("YES");
			break;
		default:
			printf("invalid!");
			break;
	}

	free(arr);
	return 0;
}