#include<stdio.h>
#include<time.h>
int main()
{
    time_t rawtime;
    struct tm *timeinfo;
    int year,month,day;
    const char *weekday[]={"Sun", "Mon", "Tue","Wedn","Thur","Fri","Sat"};

    printf("Enter year: ");fflush(stdout);scanf("%d",&year);
    printf("Enter month: ");fflush(stdout);scanf("%d",&month);
    printf("Enter day: ");fflush(stdout);scanf("%d",&day);

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    timeinfo->tm_year=year-1900;
    timeinfo->tm_mon=month-1;
    timeinfo->tm_mday=day;

    printf("That day is a %s.",weekday[timeinfo->tm_wday]);

    return 0;
}    