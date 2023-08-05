#include<stdio.h>
#include<stdbool.h>
int main()
{
    bool table[10]={false};
    bool mark[10]={false};
    int num;
    scanf("%d",&num);
    while(num)
    {
        if(table[num%10]==true)
        {
            mark[num%10]=true;
        }
        else
        {
            table[num%10]=true;
        }
        num/=10;
    } 
    for(int i=0; i<10; i++)
        if(mark[i]==true)
            printf("%d ",i);
    return 0;
}