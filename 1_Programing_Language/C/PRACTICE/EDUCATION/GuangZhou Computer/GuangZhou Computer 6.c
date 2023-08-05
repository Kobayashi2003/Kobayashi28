/*
根据输入的用电度数，计算并输出电费总价。计价规则：
用电数低于200度，按0.5元/度计算；
用电数超过200度，但不超过300度部分按0.6元/度计费；
超出300度，超出部分按0.8元/度计费。
（输入数据范围取[0, 1000]内实数，输出结果保留至小数点后两位）

输入输出样例
输入样例1：
100
输出样例1：
50.00
输入样例2：
280
输出样例2：
148.00
注：涉及到浮点数操作建议使用 double 类型
*/

#include<stdio.h>
int main() 
{
    double num;
    scanf("%lf",&num);
    
    if(num>0&&num<=1000)
    {
        double over_300,over_200,sum=0;
        
        if(num>300)
        {
            over_300=num-300;
            sum=sum+over_300*0.8;
            num=num-over_300;
        }
        if(num>200)
        {
            over_200=num-200;
            sum=sum+over_200*0.6;
            num=num-over_200;
        }

        sum=sum+num*0.5;

        printf("%-4.2f",sum);
    }

    else printf("error\n");

    return 0;
}