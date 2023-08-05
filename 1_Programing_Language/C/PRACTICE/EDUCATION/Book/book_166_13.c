#include<stdio.h>
#include<string.h>
void Strcat(char *str1,char *str2)
{
    int len=strlen(str1);
    for(int i=0;i<10-len;i++)
        str1[len+i]=str2[i];
}
int main()
{
    char str1[10],str2[10];
    printf("Please input the str1\n");
    gets(str1);
    printf("Please input the str2\n");
    gets(str2);
    Strcat(str1,str2);
    puts(str1);
    return 0;
}