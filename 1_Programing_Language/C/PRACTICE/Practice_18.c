#include<stdio.h>
#include<string.h>
#define N 50
int main()
{
    int cont=0,maxLen=0,i=0;
    char str[N]={'\0'},*flag,*flag_tmp;
    scanf("%[^\n]",str);
    while(i<strlen(str))
    {
        for (;;)
        {
            i++;
            if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z'))
            {
                if (cont == 0)
                    flag_tmp = &str[i];
                cont++;
            }
            else break;
        }
        if(cont>maxLen)
        {
            flag=flag_tmp;
            maxLen=cont;
        }
        cont=0;
    }
    for(i=0;i<maxLen;i++)
    {
        printf("%c",*(flag+i));
    }
    return 0;
}