#include <stdio.h>

int main() {

    float price; int num;
    float sum;

    while (scanf("%f %d",&price,&num) != EOF) {
        sum += price*num;
    }

    printf("%.2f",sum);

    return 0;
}