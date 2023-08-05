#include<stdio.h>
int main()
{
    const char *Month[]={"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"};
    int month;
    scanf("%d",&month);
    printf("%s",Month[month-1]);
    return 0;
}