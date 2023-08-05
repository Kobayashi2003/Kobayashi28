#include<stdio.h>
#include<string.h>
#define LEN 50
int main()
{
    char str[LEN]={'\0'},word[LEN]={'\0'};
    int i,j,len=0;
    scanf("%[^\n]",str);
    for(i=strlen(str);i>=0;i--)
    {
        if(str[i]!=' ')word[len++]=str[i];
        if(str[i]==' '||i==0)
        {
            for(j=len-1;j>=0;j--)
            {
                printf("%c",word[j]);
                word[j]='\0';
            }
            len=0;
            putchar(' ');
        } 
    }
    return 0;
}