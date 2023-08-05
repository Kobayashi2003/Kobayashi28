#include<stdio.h>
#define N 10
#define LETTER (text[i]>='A'&&text[i]<='Z')||(text[i]>='a'&&text[i]<='z')
void print(char *tmp,int len)
{
    for(int j=len-1;j>=0;j--)
    {
        printf("%c",tmp[j]);
    }
}
int main()
{
    char text[]="boy meets girl";
    char tmp[N]={'\0'};
    int len=0;
    for(int i=sizeof(text)/sizeof(char)-1;i>=0;i--)
    {
        if(LETTER)
        {
            tmp[len++]=text[i];
            if(i==0)
            {
                print(tmp,len);
                len=0;
            }

        }
        else if((!LETTER))
        {
            print(tmp,len);
            len=0;
            printf("%c",text[i]);
        }
    }
    return 0;
}