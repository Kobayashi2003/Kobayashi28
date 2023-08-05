#include<stdio.h>
#include<string.h>
int main()
{
    char str[200000];
    int num=0;
    for(int i=0;i<200000;i++)
    {
        str[i]=getchar();
        if(str[i]=='\n')
        break;
        num++;
    }

    int num_letters=0,num_numbers=0,num_blanks=0,num_others=0;

    for(int i=0;i<num;i++)
    {
        if((str[i]>='a'&&str[i]<='z')||(str[i]>='A'&&str[i]<='Z'))
        num_letters++;
        else if(str[i]>='0'&&str[i]<='9')
        num_numbers++;
        else if(str[i]==' ')
        num_blanks++;	
        else
        num_others++;
    }

    printf("num_letters: %d\nnum_numbers: %d\nnum_blanks: %d\nnum_others: %d\n",num_letters,num_numbers,num_blanks,num_others);

    return 0;
    
}