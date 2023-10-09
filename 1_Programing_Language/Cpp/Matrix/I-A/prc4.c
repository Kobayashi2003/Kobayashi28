#include <stdio.h>
#include <math.h>

int main() {

    int a, b, c; scanf("%d %d %d", &a, &b, &c); 

    double delta = pow(b, 2) - 4 * a * c;

    if (delta < 0) {

    } else {
        double x1 = (-b + sqrt(delta)) / (2 * a);
        double x2 = (-b - sqrt(delta)) / (2 * a);
        if (x1 < x2) {
            printf("%.2lf %.2lf", x1, x2);
        } else {
            printf("%.2lf %.2lf", x2, x1);
        }
    }

    return 0;
}