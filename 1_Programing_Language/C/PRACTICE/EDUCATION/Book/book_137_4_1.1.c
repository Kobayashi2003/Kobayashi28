#include<stdio.h>
int main()
{
    int num_letters=0,num_numbers=0,num_blanks=0,num_others=0;
    for(char c;(c=getchar())!='\n';)
    {
        if((c>='a'&&c<='z')||c>='A'||c>='Z')num_letters++;
        else if(c>='0'&&c<='9')num_numbers++;
        else if(c==' ')num_blanks++; 
        else num_others++;
    }
    printf("num_letters: %d\nnum_numbers: %d\nnum_blanks: %d\nnum_others: %d\n",num_letters,num_numbers,num_blanks,num_others);
    return 0;
}