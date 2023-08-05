//找出一个字符串中第一个重复的字母 首次使用简单的哈希表
#include<stdio.h>
#include<string.h>
#define N 10
int main()
{
    char str[N]={'\0'};
    int Index[26]={0};
    scanf("%s",str);
    strlwr(str);
    for(int i=0;str[i]!='\0';i++)
    {
        Index[str[i]-'a']++;
        if(Index[str[i]-'a']>1)
        {
            printf("%c\n",str[i]);
            return 0;
        }
    }
    printf("-1\n");
    return 0;
}