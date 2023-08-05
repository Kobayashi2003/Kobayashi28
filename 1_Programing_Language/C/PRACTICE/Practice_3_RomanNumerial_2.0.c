#include<stdio.h>
#include<stdlib.h>
#include<string.h>
const int value[]={1000,900,500,400,100,90,50,40,10,9,5,4,1};
const char *symbol[]={"M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"};
char *intoRoman(int num)
{
    char *roman=(char *)malloc(sizeof(char)*16);
    roman[0]='\0';
    for(int i=0;i<13;i++)
    {
        while(num>=value[i])
        {
            num-=value[i];
            strcpy(roman+strlen(roman),symbol[i]);
        }
    }
    return roman;
} 
int main()
{
    int num;
    char *roman;
    scanf("%d",&num);
    roman=intoRoman(num);
    printf("%s\n",roman);
    return 0;
}