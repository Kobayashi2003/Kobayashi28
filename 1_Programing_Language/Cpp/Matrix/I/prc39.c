#include <stdio.h>

#define N 64 

typedef struct Date
{
    int year;
    int month;
    int day;
} Date;

int countDate(Date date) {
    int days = 0;
    int monthDays[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
    if (date.year % 4 == 0 && date.year % 100 != 0 || date.year % 400 == 0) {
        monthDays[1] = 29;
    }
    for (int i = 0; i < date.month-1; ++i) {
        days += monthDays[i];
    }
    days += date.day;
    return days;
}

int main() {
    Date dates[N];
    int n; scanf("%d", &n);
    for (int i = 0; i < n; ++i) {
        scanf("%d %d %d", &dates[i].year, &dates[i].month, &dates[i].day);
    }

    for (int i = 0; i < n; ++i) {
        printf("%d\n", countDate(dates[i]));
    }

    return 0;
}