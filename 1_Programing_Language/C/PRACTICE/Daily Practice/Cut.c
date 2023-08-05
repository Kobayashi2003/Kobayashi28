#include<stdio.h>
#include<string.h>
int main()
{
    char buf[]="Chian";
    int count=2;
    char str_1[12],str_2[12];
    for(int i=0;i<12;i++)
    {
        if(i<count)str_1[i]=buf[i];
        if(i>count)str_2[i-count-1]=buf[i];
    }
    memset(buf,'\0',sizeof(buf));
    strcat(buf,str_1);
    strcat(buf,str_2);
    printf("%s",buf);
    return 0;
}