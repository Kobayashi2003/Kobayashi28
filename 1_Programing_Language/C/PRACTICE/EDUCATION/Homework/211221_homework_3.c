/*输入一个字符串，内有数字和非数字字符，例如
A123x456 17960? 302tab5876
将其中连续的数字作为一个整数，依次存放到一数组a中。例如123放到a[0]，456放到a[1]... 统计共有多少个整数，并输出这些数。
（要求用指针方法处理）
*/
#include<stdio.h>
#include<string.h>
#define N 100
#define Save 1
#define Jump 0
char saveArray[N][N]={'\0'};
int saveNum[N]={0}; 
int count=0;
int Pow(int x,int y)
{
    int res=1;
    for(int i=0;i<y;i++)res*=x;
    return res;
}
void Change(int ord)//将该数转换为整型的数
{
    int len=strlen(saveArray[ord]);
    int num=0;
    for(int i=0,j=len-1;i<len;i++,j--)
        num+=(saveArray[ord][i]-'0')*Pow(10,j);
    saveNum[ord]=num;
}
void selectArray(char *str,char *head,char *tail)//定义函数 用于选出字符串中的数字
{
    int state;//定义变量 用于确定是否进行储存
    if(*head>='0'&&*head<='9')state=Save;
    else state=Jump;
    switch(state)
    {
        case Save:
        for(int i=0;(*head>='0'&&*head<='9')&&head!=tail;i++,head++)
            saveArray[count][i]=*head;
        count++;
        break;

        case Jump:
        while((*head<'0'||*head>'9')&&(head!=tail))head++;
        break;
    }
    if(head!=tail) selectArray(str,head,tail);
}
int main()
{
    char str[N]={'\0'};
    scanf("%[^\n]",str);
    strcat(str,"E");
    selectArray(str,str,&str[strlen(str)-1]);
    for(int i=0;i<count;i++) 
    {
        Change(i);
        printf("the %d number is:%d",i+1,saveNum[i]);
        putchar('\n');
    } 
    return 0;
}

/*
#include<stdio.h>
#include<string.h>
#define N 100
#define Save 1
#define Jump 0
char saveArray[N][N]={'\0'};
int saveNum[N]={0};
int count=0;
int Pow(int x,int y)
{
    int res=1;
    int i;
    for(i=0;i<y;i++)res*=x;
    return res;
}
void Change(int ord)
{
    int len=strlen(saveArray[ord]);
    int num=0;
    int i,j;
    for(i=0,j=len-1;i<len;i++,j--)
        num+=(saveArray[ord][i]-'0')*Pow(10,j);
    saveNum[ord]=num;
}
void selectArray(char *str,char *head,char *tail)
{
    int i;
    int state;
    if(*head>='0'&&*head<='9')state=Save;
    else state=Jump;
    switch(state)
    {
        case Save:
        for(i=0;(*head>='0'&&*head<='9')&&head!=tail;i++,head++)
            saveArray[count][i]=*head;
        count++;
        break;

        case Jump:
        while((*head<'0'||*head>'9')&&(head!=tail))head++;
        break;
    }
    if(head!=tail) selectArray(str,head,tail);
}
int main()
{
    int i;
    char str[N]={'\0'};
    scanf("%[^\n]",str);
    strcat(str,"E");
    selectArray(str,str,&str[strlen(str)-1]);
    for(i=0;i<count;i++) 
    {
        Change(i);
        printf("the %d number is:%d",i+1,saveNum[i]);
        putchar('\n');
    } 
    return 0;
}
*/