#include <stdio.h>

#define MAX 2048

int main() {

    int M; int N; scanf("%d %d", &N, &M);

    int nums[MAX][3] = {0};
    int count = 0;

    if (M * 5 == N) {
        nums[count][0] = M;
        count += 1;
    }

    for (int i = M; i >=0; --i) {
        if (i*5 < N) {
            nums[count][0] = i;
            int rest = N - i*5;
            for (int j = M-i; j >= 0; --j) {
                if (j*3 <= rest) {
                    if (i + j + (rest-j*3) * 3 != M) continue;
                    nums[count][1] = j; nums[count][2] = (rest-j*3) * 3;
                    count += 1;
                    nums[count][0] = i;
                }
            }
        }
    }

    for (int i = 0; i < count; ++i) {
        if (nums[i][0] + nums[i][1] + nums[i][2] == M)
            printf("%d %d %d\n", nums[i][0], nums[i][1], nums[i][2]);
    }
    if (count == 0) printf("no answer\n");

    return 0;
}