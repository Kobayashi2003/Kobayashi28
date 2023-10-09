#include <stdio.h>
#include <math.h>

int main() {

    int a, b, c; scanf("%d%d%d", &a, &b, &c);

    double delta = pow(b, 2) - 4 * a * c;

    if (delta < 0)
        printf("None\n");
    else if (delta == 0)
        printf("%.2lf\n", -b / (2.0 * a));
    else {
        double x1 = (-b + sqrt(delta)) / (2.0 * a);
        double x2 = (-b - sqrt(delta)) / (2.0 * a);
        if (x1 > x2)
            printf("%.2lf %.2lf\n", x2, x1);
        else
            printf("%.2lf %.2lf\n", x1, x2);
    }


    return 0;
}