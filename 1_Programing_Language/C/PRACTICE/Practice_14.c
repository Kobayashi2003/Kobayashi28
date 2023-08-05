//a不比x c不比x，z
#include<stdio.h>
int main()
{
    char a,b,c;
    char enermy[]={"yxz"};
    for(int i=0;i<3;i++)
    {
        if(enermy[i]!='x' &&enermy[i]!='z')
            c=enermy[i];
        else if(enermy[i]!='x')
            a=enermy[i];
        else 
            b=enermy[i];
    }
    printf("%c %c %c\n",a,b,c);
    return 0;
}