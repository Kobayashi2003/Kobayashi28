#include<stdio.h>
#define N 10
int main()
{
    char str[N]={'\0'},*p_str=str;
    int num[N]={0},*p_num=num,i,ord=0,flg=0;
    scanf("%[^\n]",str);
    for(i=0;*(p_str+i)!='\0'&&i<N;i++)
    {
        if(*(p_str+i)>='0'&&*(p_str+i)<='9')
        {
            *(p_num+ord)=*(p_str+i)+*(p_num+ord)*10-'0';
            flg=1;
        }
        else if(flg!=0)
        {
            ord++;
            flg=0;
        }
    }
    for(i=0;i<=ord;i++)
        printf("the %d number is:%d\n",i+1,*(p_num+i));
    return 0;
}

/*
#include<stdio.h>
#define N 10
int main()
{
    char str[N]={'\0'}; 
    int num[N]={0},i,cont=0,flg=0;
    scanf("%[^\n]",str);
    for(i=0;str[i]!='\0'&&i<N;i++)
    {
        if(str[i]>='0'&&str[i]<='9')
        {
            num[cont]=str[i]+num[cont]*10-'0';
            flg=1;
        }
        else if(flg!=0)
        {
            cont++;
            flg=0;
        }
    }
    for(i=0;i<=cont;i++)
        printf("the %d number is:%d\n",i+1,num[i]);
    return 0;
}
*/