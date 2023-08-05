#include<stdio.h>
#include<string.h>
#define N 100
void Staticsticker(char *str,int *p_num,int *p_let,int *p_bla,int *p_oth,int len)
{
    for(int i=0;i<len;i++){
        if(str[i]>='0'&&str[i]<='9')(*p_num)++;
        else if((str[i]>='a'&&str[i]<'z')||(str[i]>='A'&&str[i]<='Z'))(*p_let)++;
        else if(str[i]==' ')(*p_bla)++;
        else (*p_oth)++;
    }
}
int main()
{
    char str[N]={'\0'};
    gets(str);
    int numbers=0,letters=0,blanks=0,others=0;
    int *p_num=&numbers,*p_let=&letters,*p_bla=&blanks,*p_oth=&others;
    Staticsticker(str,p_num,p_let,p_bla,p_oth,strlen(str));
    printf("%s\nnumbers:%d\nletters:%d\nblanks:%d\nothers:%d\n",str,numbers,letters,blanks,others);
    return 0;
}