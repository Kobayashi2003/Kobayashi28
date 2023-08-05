#include<stdio.h>
#include<string.h>
const int Month[]={31,28,31,30,31,30,31,31,30,31,30,31};//定义月份对照表
int leapYear(int year){
    return ((year%400==0)||(year%100!=0&&year%4==0));//判断该年是否为润年，若为闰年，则返回1；否则返回0
}
void whichDay(int year,int month,int day)
{
    int sum=day;
    int i;
    for(i=0;i<month-1;i++) sum+=Month[i];//参照对照表，将该月前的所有月份的总天数加到sum上
    if(month>2) sum+=leapYear(year);//若该月所在年份为润年且该月在二月的后面，则sum加1
    printf("It is the %d day in this year\n",sum);
}
int main()
{
    int year,month,day;
    printf("Please enter the year:\n");
    scanf("%d",&year);
    printf("Please enter the month:\n");
    scanf("%d",&month);
    printf("Please enter the day:\n");
    scanf("%d",&day);
    whichDay(year,month,day);
    return 0;
}