#include<stdio.h>
#include<string.h>
int main()
{
    char array[30];
    gets(array);
    int len=strlen(array);
    for(int i=0,j=len-1;j-i>1;i++,j--)
    {
        int temp=array[i];
        array[i]=array[j];
        array[j]=temp;
    }
    printf("%s", array);
    return 0;
}