#include <stdio.h>
#include<math.h>

#define M_PI 3.14

int main() {
    
    double l, r; 
    scanf("%lf", &l);
    scanf("%lf", &r);


    double square_area = l * l;
    double circle_area = M_PI * r * r;

    printf("the area of the square is %.2lf\n", square_area);
    printf("the area of the circle is %.5lf\n", circle_area);

    return 0;
}