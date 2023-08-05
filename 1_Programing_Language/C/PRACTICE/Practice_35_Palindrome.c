//回文检测
#include<stdio.h>
#include<malloc.h>
#include<string.h>
int main()
{
    char text[]="He lived as a devil, eh?";
    strupr(text);
    int len=1,cont=0;
    char *save=(char*)malloc(len*sizeof(char));
    for(int i=0;i<sizeof(text)/sizeof(char)-1;i++)
    {
        if(text[i]>='A'&&text[i]<='Z')
        {
            if(cont==len)
            {
                len++;
                save=(char*)realloc(save,len*sizeof(char));
            }
            save[cont]=text[i];
            cont++;
        }
    }
    char *low=&save[0],*high=&save[len-1];
    while(low<high)
    {
        if(*low!=*high)
        {
            printf("Not palindrome.\n");
            return 0;
        }
        low++;
        high--;
    }
    printf("Is palindrome.\n");
    return 0;
}