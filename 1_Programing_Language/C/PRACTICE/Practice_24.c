#include<stdio.h>
int main()
{
    int days,day;
    printf("Enter number of days in month:");
    scanf("%d",&days);
    printf("Enter starting day of the week:");
    scanf("%d",&day);
    printf("%s %s %s %s %s %s %s\n",
        "SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIEND","SATURDAY");
    for(int j=1; j<day; j++)
        printf("\t");
    for(int i=1; i<=days; i++)
    {
        printf("%3d\t",i);
        if((i+day-1)%7==0) printf("\n");
    }
    return 0;
}