#include<stdio.h>
#include<string.h>
#define N 10
void insert(char *str1,char *str2,int n)
{
    int len1=strlen(str1),len2=strlen(str2);
    int i;
    for(i=0;i<len1-n;i++)
    {
        str1[n+len2+i]=str1[n+i];
    }
    for(i=0;i<len2;i++)
    {
        str1[n+i]=str2[i];
    }
    printf("the new string is:%s the lenth of the new string is:%d",str1,strlen(str1));
}
int main()
{
    int n;
    char str1[2*N]={'\0'},str2[N]={'\0'};
    printf("Please enter the first string:\n");
    scanf("%[^\n]",str1);
    getchar();
    printf("Please enter the second string:\n");
    scanf("%[^\n]",str2);
    printf("Please enter the place you want to insert:\n");
    scanf("%d",&n);
    insert(str1,str2,n);
    return 0;
}