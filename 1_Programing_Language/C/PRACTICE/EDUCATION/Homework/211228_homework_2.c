#include<stdio.h>
#define the_first_day 2
typedef struct DATE//定义结构体
{
    int year;
    int month;
    int day;
}DATE;
const int Month[]={31,28,31,30,31,30,31,31,30,31,30,31};//定义月份对照表
const char *Day[]={"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};//定义星期对照表
int leapYear(int year){
    return ((year%400==0)||(year%100!=0&&year%4==0));//判断该年是否为润年，若为闰年，则返回1；否则返回0
}
void whichDay(DATE *p_date)
{
    int sum=p_date->day;
    int i;
    for(i=0;i<p_date->month-1;i++) sum+=Month[i];//参照对照表，将该月前的所有月份的总天数加到sum上
    if(p_date->month>2) sum+=leapYear(p_date->year);//若该月所在年份为润年且该月在二月的后面，则sum加1
    printf("It is the %d day in this year\n",sum);
    printf("The day is %s\n",Day[the_first_day+sum%7-2]);
}
int main()
{
    DATE date,*p_date=&date; 
    printf("Please enter the year:\n");
    scanf("%d",&p_date->year);
    printf("Please enter the month:\n");
    scanf("%d",&p_date->month);
    printf("Please enter the day:\n");
    scanf("%d",&p_date->day);
    whichDay(p_date);
    return 0;
}