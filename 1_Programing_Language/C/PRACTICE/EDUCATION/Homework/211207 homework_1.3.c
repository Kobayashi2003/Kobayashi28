#include<stdio.h>
int main()
{
    float average(float array[],int n);
    float score1[5]={98.5,97,91.5,60,55};
    float score2[10]={98.5,97,91.5,60,55,83,93,34,43,23.5};
    printf("The average of the class A is %6.2f\n",average(score1,5));
    printf("The average of the class B is %6.2f\n",average(score2,10));
    return 0;
}
float average(float array[],int n)
{
    int i;
    float aver,sum=array[0];
    for(i=1;i<n;i++)
        sum=sum + array[i];
    aver=sum/n;
    return aver;
}