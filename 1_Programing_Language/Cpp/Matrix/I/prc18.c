#include<stdio.h>
#include<math.h>
// #include "mytriangle.h"


double triangle(int a, int b, int c) {
    if  (a + b <= c || a + c <= b || b + c <= a)
        return 0;
    double p = (a + b + c) / 2.0;
    double S = sqrt(p * (p - a) * (p - b) * (p - c));
    return S;
}


int main(){
	int a,b,c;
	scanf("%d %d %d", &a, &b, &c);
	double S = triangle(a,b,c);
	printf("%.4lf",S);
	return 0;
}