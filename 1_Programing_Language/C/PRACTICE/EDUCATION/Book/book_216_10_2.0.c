#include<stdio.h>
#include<string.h>
#define N 20
void longestWord(char *str,int len)
{
    int maxLen=0,len_tmp,mark=-1,flag;
    for(int i=0;i<len;i++)
    {
        if(str[i]==' ')
        {
            len_tmp=i-mark-1;
            if(len_tmp>maxLen)
            {
                flag=mark+1;
                maxLen=len_tmp;
            }
            mark=i;
        }
    }
    for(int i=flag;i<flag+maxLen;i++)
        printf("%c",str[i]);
}
int main()
{
    char str[N]={'\0'};
    gets(str);
    str[strlen(str)]=' ';
    longestWord(str,strlen(str));
    return 0;
}