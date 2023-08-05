#include<stdio.h>
#include<string.h>
#define N 22
void fun(char *arry)
{
    char *tmp=&arry[1];
    int cont_num=0,cont_let=0,len=strlen(arry),i,j;
    arry[0]=arry[len-1]='\0';
    strcpy(arry,tmp);
    for(i=0;i<(len=strlen(arry));i++)
    {
        for(j=i+1;j<len;j++)
        {
            if(arry[i]>arry[j])
            {
                arry[i]^=arry[j];
                arry[j]^=arry[i];
                arry[i]^=arry[j];
            }
        }
        if(arry[i]>='0'&&arry[i]<='9') cont_num++;
        else if((arry[i]>='A'&&arry[i]<='Z')||(arry[i]>='a'&&arry[i]<='z')) cont_let++;
    }
    printf("arry:%s number:%d letter:%d\n",arry,cont_num,cont_let);
}
int main()
{
    char arry[N]={'\0'};
    scanf("%[^\n]",arry);
    fun(arry);
    return 0;
}
/*自定义函数：fun(char arry[])，对读入的字符串，去掉首尾两个字符，其余字符按ASCII码降序排序；对于排序后的剩余字符串统计字母的个数和数字的个数。
主函数中：键盘读入一个字符串，调用函数fun，打印：1）排序后的剩余字符串；2）排序后的字符串中字母的个数；3）排序后的字符串中数字的个数。
例如：
输入：a5cGf3*
输出：
fcG53
character:3
number:2
*/
//1.删首尾 2.降序排序 3.字母个数 数字个数