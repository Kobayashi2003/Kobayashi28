#include <stdio.h>
#include <math.h>

#define M_PI 3.14

int main() {
    
    double l, r; 
    scanf("%lf", &l);
    scanf("%lf", &r);


    double square_area = l * l;
    double circle_area = M_PI * r * r;

    // the number ouput with 14 char width 
    char buffer[100] = {0};
    // printf("the area of the square is ");
    sprintf(buffer, "the area of the square is %014.3f\n", square_area);
    sprintf(buffer, "%sthe area of the circle is %014.5f\n", buffer, circle_area);

    printf("%s", buffer);

    return 0;
}