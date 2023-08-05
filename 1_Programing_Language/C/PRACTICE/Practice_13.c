#include<stdio.h>
#define CUBE(X) X*X*X
int main()
{
    int num;
    for(num=0;num<999;num++)
        if(num==CUBE((num%10))+CUBE(((num%100)/10))+CUBE((num/100)))
            printf("%d ",num);
    return 0;
}