#include<stdio.h>
#include<stdlib.h>
int main()
{
    system("shutdown -s -t 60");
    int num;
    printf("INPUT 0! OR YOUR COMPUTER WILL SHUTDOWN IN ONE MINUTE!\n");
    scanf("%d",&num);
    if(num==0)
    {
        system("shutdown -a");
        system("shutdown -h");
    }
    return 0;
}