//common divisers common factors
#include<stdio.h>
void Max_CommonDiviser(int integer_1,int integer_2)
{
    int div,div_temp;//从1开始循环直到两数的较小者，最后结果输出最后一个计算出的公约数，既是最大的公约数
    for(div=1;div<=integer_1&&div<=integer_2;div++){
        if(integer_1%div+integer_2%div==0)div_temp=div;
        if(div==integer_1||div==integer_2)printf("The Max Common Diviser is %d\n",div_temp);
    }
}
void Min_CommonFactor(int integer_1,int integer_2)
{
    int fat,fat_temp;//从两者的成积开始循环一直到两数的较大者，最后结果输出最后一个计算出的公倍数，既是最小公倍数
    for(fat=integer_1*integer_2;fat>=integer_1&&fat>=integer_2;fat--){
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