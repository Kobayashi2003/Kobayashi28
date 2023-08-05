//common divisers common factors
#include<stdio.h>
void Max_CommonDiviser(int integer_1,int integer_2)
{
    for(int div=1,div_temp;div<=integer_1&&div<=integer_2;div++){
        if(integer_1%div+integer_2%div==0)div_temp=div;
        if(div==integer_1||div==integer_2)printf("The Max Common Diviser is %d\n",div_temp);
    }
}
void Min_CommonFactor(int integer_1,int integer_2)
{
    for(int fat=integer_1*integer_2,fat_temp;fat>=integer_1&&fat>=integer_2;fat--){
        if(fat%integer_1+fat%integer_2==0)fat_temp=fat;
        if(fat==integer_1||fat==integer_2)printf("The Min Common Factor is %d\n",fat_temp);
    }
}
int main()
{
    int integer_1,integer_2;
    scanf("%d %d",&integer_1,&integer_2);
    Max_CommonDiviser(integer_1,integer_2);
    Min_CommonFactor(integer_1,integer_2);
    return 0;
}