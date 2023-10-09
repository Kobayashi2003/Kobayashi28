#include <stdio.h>

int main() {

    double sum1 = 0, sum2 = 0, sum3 = 0, sum4 = 0;

    int data1, data2, data3;

    for (int i = 0; i < 3; ++i) {
        scanf("%d %d %d", &data1, &data2, &data3);
        sum1 += data1;
        sum2 += data2;
        sum3 += data3;
        double sum_tmp = data1 + data2 + data3;
        sum4 += sum_tmp;
        printf("%.2lf", sum_tmp); 
        if (i != 2) printf(" ");
    }
    printf("\n");

    printf("%.2lf %.2lf %.2lf %.2lf", sum4/3, sum1/3, sum2/3, sum3/3);

    return 0;
}