//ROMAN NUMERAL
//SPECIAL IV 4  IX 9  XL 40  XC 90  CD 400  CM 900
#include<stdio.h>
#define I 1
#define V 5
#define X 10
#define L 50
#define C 100
#define D 500
#define M 1000 
void RomanNumeral(int num) 
{
    if(num==4)printf("IV");
    else if(num==9)printf("IX");
    else if(num==40)printf("XL");
    else if(num==90)printf("XC");
    else if(num==400)printf("CD");
    else if(num==900)printf("CM");
    else
    {    
        int num_M=0,num_D=0,num_C=0,num_L=0,num_X=0,num_V=0,num_I=0;
        num_M=num/M;
        if(num_M!=0)
            num=num%M;
        num_D=num/D;
        if(num_D!=0)
            num=num%D;
        num_C=num/C;
        if(num_C!=0)
            num=num%C;
        num_L=num/L;
        if(num_L!=0)
            num=num%L;
        num_X=num/X;
        if(num_X!=0)
            num=num%X;
        num_V=num/V;
        if(num_V!=0)
            num=num%V;
        num_I=num/I;
        for(int i=1;i<=num_M;i++)
            printf("M");
        for(int i=1;i<=num_D;i++)
            printf("D"); 
        for(int i=1;i<=num_C;i++)
            printf("C");
        for(int i=1;i<=num_L;i++)
            printf("L");
        for(int i=1;i<=num_X;i++)
            printf("X");
        for(int i=1;i<=num_V;i++)
            printf("V");
        for(int i=1;i<=num_I;i++)
            printf("I");
    }
    }
int main()
{
    int num;
    scanf("%d", &num);
    RomanNumeral(num);
    return 0;
}