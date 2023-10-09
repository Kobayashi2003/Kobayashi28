#include <stdio.h>

int main() {

    float sum = .0f, tmp = .0f;
    int n = 0;

    while (scanf("%f", &tmp) && (tmp != -1)) {
        printf("%f,", tmp);
        sum += tmp;
        if (tmp > 0)
            n++;
    }
    // printf("%f\n", tmp);
    printf("\n");

    if (n != 0)
        printf("Raindays %d, average rainfall %f.", n, sum / n);
    else 
        printf("No rain."); 

    return 0;
}