#include<stdio.h>
int main()
{
    int sum,year,month,day,Month[12]={31,28,31,30,31,30,31,31,30,31,30,31};
    scanf("%d %d %d",&year,&month,&day);
    if((year%400==0)||(year%4==0&&year%100!=0))Month[1]++;
    for(int i=0;i<month-1;i++)sum+=Month[i];
    printf("%d",sum+day);
    return 0;    
}

//我可真是个大聪明