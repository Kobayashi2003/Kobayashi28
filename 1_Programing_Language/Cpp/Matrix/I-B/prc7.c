#include <stdio.h>

#define MAX_M 100

#define MAX(a, b) ((a) > (b) ? (a) : (b))

void sortByLeft(int areas[][2], int M) {
    for (int i = 0; i < M; ++i) {
        for (int j = i + 1; j < M; ++j) {
            if (areas[i][0] > areas[j][0]) {
                int tmp = areas[i][0];
                areas[i][0] = areas[j][0];
                areas[j][0] = tmp;

                tmp = areas[i][1];
                areas[i][1] = areas[j][1];
                areas[j][1] = tmp;
            }
        }
    }
}

int merge(int areas[][2], int M) {
    sortByLeft(areas, M);
    int areas_merged[MAX_M][2];
    int count = 0;
    for (int i = 0; i < M; ++i) {
        int L = areas[i][0], R = areas[i][1];
        if (count == 0 || areas_merged[count - 1][1] < L) {
            areas_merged[count][0] = L;
            areas_merged[count][1] = R;
            ++count;
        } else {
            areas_merged[count - 1][1] = MAX(areas_merged[count - 1][1], R);
        }
    }

    for (int i = 0; i < count; ++i) {
        areas[i][0] = areas_merged[i][0];
        areas[i][1] = areas_merged[i][1];
    }

    return count;
}

int main() {

    int L, M; scanf("%d%d", &L, &M);

    int areas[MAX_M][2];
    for (int i = 0; i < M; ++i) {
        int left, right; scanf("%d%d", &left, &right);
        areas[i][0] = left;
        areas[i][1] = right;
    }

    int count = merge(areas, M);
    for (int i = 0; i < count; ++i) {
        L -= areas[i][1] - areas[i][0] + 1;
    }

    printf("%d\n", L+1);

    return 0;
}