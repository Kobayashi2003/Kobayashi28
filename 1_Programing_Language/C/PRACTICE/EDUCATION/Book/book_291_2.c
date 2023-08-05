#include<stdio.h>
#include<string.h>
#define N 3
void Compare(char *p_str1,char *p_str2,char *p_str3)
{
    char *str[]={p_str1,p_str2,p_str3};
    for(int i=0;i<3;i++)
        for(int j=i;j<3;j++)
            if(strcmp(str[i],str[j])>0)
            {
                *str[i]^=*str[j];
                *str[j]^=*str[i];
                *str[i]^=*str[j];
            }
}
int main()
{
    char str1[N]={'\0'},str2[N]={'\0'},str3[N]={'\0'};
    char *p_str1=str1,*p_str2=str2,*p_str3=str3;
    scanf("%s%s%s",str1,str2,str3);
    Compare(p_str1,p_str2,p_str3);
    printf("%s\n%s\n%s\n",str1,str2,str3);
    return 0;
}