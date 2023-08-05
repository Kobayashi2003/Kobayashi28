//宏常量
//CLOCKS_PER_SEC 滴答声/秒 时间的单位
//NULL 空指针

//clock_t 时钟类型
//size_t 无符号类型
//time_t 时间类型 表示时间

//struct tm 时间结构 包括日历、时间
//tm_sec seconds
//tm_min minutes
//tm_hour hours
//tm_mday month day of the month 1-31
//tm_mon months since January 0-11
//tm_year years since 1900
//tm_wday week days since Sunday 0-6
//tm_yday years days since January 1st 0-365
//tm_isdst Daylight saving time flag
/*
#include<stdio.h>
#include<time.h>

clock_t clock(void)

int main()
{
    clock_t t;
    t=clock()-t;
    printf("%d\n%f\n",t,((float)t)/CLOCKS_PER_SEC);
    return 0;
}

double difftime(time_t end,time_t beginning)

int main()
{
    time_t now;
    struct tm newyear;
    double seconds;
    time(&now);//get current time;same as: now=time(NULL)
    newyear=*localtime(&now);
    newyear.tm_hour=0;
    newyear.tm_min=0;
    newyear.tm_sec=0;
    newyear.tm_mon=0;
    newyear.tm_mday=1;
    seconds=difftime(now,mktime(&newyear));
    printf("%.f seconds since new year in the current timezone.\n",seconds);
    return 0;
}

time_t mktime(struct tm *timeptr)
    返回timepter指针描述的时间，如果时间未描述，返回-1
    localtime的逆变换

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
*/


#include<stdio.h>
#include<time.h>
#define N 10
#define Mark 1
int main()
{
	int isEmpty(int *Table);
	void selectIntersection(int *array_1,int *array_2,int n1,int n2);
	int i;
    int array_1[N]={0},array_2[N]={0};
    int n1,n2;
    printf("Please enter the number of elements in the first array:\n");
    scanf("%d",&n1);
    printf("Please enter the elements in the first array:\n");
    for(i=0;i<n1;i++)
        scanf("%d",&array_1[i]);
    printf("Please enter the number of elements in the second array:\n");
    scanf("%d",&n2);
    printf("Please enter the elements in the second array:\n");
    for(i=0;i<n2;i++)
        scanf("%d",&array_2[i]);

    clock_t t;
    t=clock();

    selectIntersection(array_1,array_2,n1,n2);

    t=clock()-t;
    printf("time:\nclick:%d\nsecond:%f\n",t,((float)t)/CLOCKS_PER_SEC);
    
    return 0;
}
int isEmpty(int *Table)
{
	int i;
    int count=0;
    for(i=0;i<N;i++)
        if(Table[i]==Mark)count++;
    return count;
}
void selectIntersection(int *array_1,int *array_2,int n1,int n2)
{
	int i,j;
    int Table[N]={0};
    for(i=0;i<n1;i++)
        for(j=0;j<n2;j++)
            if(array_1[i]==array_2[j])
            {
                if(Table[j]!=Mark)
                {
                    Table[j]=Mark;
                    break;
                }
            }
    if(isEmpty(Table)!=0)
    {
		int i;
        for(i=0;i<n1;i++)
            if(Table[i]==Mark)printf("%-2d",array_2[i]);
        putchar('\n');
    }
    else printf("No Intersection!\n");
}