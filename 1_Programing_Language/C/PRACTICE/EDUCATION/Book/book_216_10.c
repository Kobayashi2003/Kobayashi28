//在这里没有考虑多个单词长度相等时的情况，若要考虑，可尝试使用多维数组对单词进行储存
//第一次运用分支储存结构，代码过于冗长，需要后期的算法优化
#include<stdio.h>
#include<string.h>
#define N 100
void Which_is_the_Longest_Letter(char *str,int len)
{
    char temp[10]={'\0'};
    int On_Off=1,count_1=0,count_2=0;
    for(int i=0,len_temp=0;i<len;i++)
    {
        if(str[i]==' ')On_Off^=1;
        switch(On_Off)
        {
            case 1:
            if(str[i]!=' ')count_1++;
            count_2^=count_2;
            break;

            case 0:
            if(str[i]!=' ')count_2++;
            count_1^=count_1;
            break;
        }

        int count=(count_1>count_2)?count_1:count_2;
        if(count>=len_temp)
        {
            len_temp=count;
            for(int j=0;j<len_temp;j++)
                temp[j]=str[i+j-len_temp+1];
        }  
    }
    puts(temp);
}
int main()
{
    char str[N]={'\0'};
    for(int i=0;(str[i]=getchar())!='\n';i++)
    str[strlen(str)]=' ';
    Which_is_the_Longest_Letter(str,strlen(str));
    return 0;
}
