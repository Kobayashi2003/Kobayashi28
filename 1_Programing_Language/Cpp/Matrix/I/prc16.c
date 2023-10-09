#include <stdio.h>

int main() {


    short Days_in_Month[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
    short is_leap_year = 0;

    int year, month, day; scanf("%d %d %d", &year, &month, &day);

    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
        is_leap_year = 1;

    if (is_leap_year)
        Days_in_Month[1] = 29;

    int days = 0;

    for (int i = 0; i < month-1; i++) {
        days += Days_in_Month[i];
    }
    days += day;

    printf("%d\n", days);

    return 0;
}