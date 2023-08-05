#include<stdio.h>
#include<string.h>
#define N 10
#define Save 1
#define Jump 0
char saveArray[N][N]={'\0'};
int num=0;
char *state_Save(char *str,char *start,char *tail,int num)
{
    for(int i=0;(*start>='0'&&*start<='9')&&start!=tail;i++,start++){
        saveArray[num][i]=*start;
    }
    return start;
}
char *state_Jump(char *str,char *start,char*tail)
{
    while(((*start>='a'&&*start<='z')||(*start>='A'&&*start<='Z'))&&(start!=tail))start++;
    return start;
}
void selectArray(char *str,char *start,char *tail)
{
    int state;
    if(*start>='0'&&*start<='9')state=Save;
    else state=Jump;

    switch(state)
    {
        case Save:
        start=state_Save(str,start,tail,num++);
        break;
        case Jump:
        start=state_Jump(str,start,tail);
        break;
    }
    if(start!=tail)selectArray(str,start,tail);
}
int main()
{
    char str[N]={'\0'};
    printf("Please enter a string:\n");
    scanf("%s",str);
    strcat(str,"E");

    selectArray(str,str,&str[strlen(str)-1]);

    for(int i=0;i<num;i++)
        printf("The %d number is:%s\n",i+1,saveArray[i]);
    return 0;
}