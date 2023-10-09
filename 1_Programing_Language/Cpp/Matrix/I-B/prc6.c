#include <stdio.h>

int main() {

    int year = 0; scanf("%d", &year);

    if ((year % 3 == 0 && year % 100 != 0) || year % 300 == 0) 
        printf("YES");
    else
        printf("NO");

    return 0;
}