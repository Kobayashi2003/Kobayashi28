#include <stdio.h>

int main() {

    int a, b; scanf("%d %d",&a,&b);
    int rabbit = (a - b*2) / 2;
    int chicken = b - rabbit;

    printf("%d %d\n",chicken,rabbit);

    return 0;
}