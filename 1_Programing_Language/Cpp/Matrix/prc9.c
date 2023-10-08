#include <math.h>
#include <stdio.h>

#define M_PI 3.14

int main(){

    float V; scanf("%f", &V);
    float R = pow(3*V/(4*M_PI),1.0/3);
    float S = 4.0 * M_PI * pow(R,2);

    printf("%.2f", S);

    return 0;
}