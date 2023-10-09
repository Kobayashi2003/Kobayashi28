#include <stdio.h>
#include <math.h>

int main() {

    double x; scanf("%lf", &x);

    double y;
    if (abs(x) < 10)
        y = 23 + 6.5 * pow(x, 2);
    else
        y = abs(x) + 0.5;

    printf("%.2lf\n", y);

    return 0;
}