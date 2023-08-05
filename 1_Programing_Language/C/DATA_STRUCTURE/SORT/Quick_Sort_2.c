#include<stdio.h>
#define N 10
void QukSort(int *array,int *low,int *high,int num)
{
    if(low==high) return;

    int *tmp_low=low,*tmp_high=high;

    while(*high>=num&&high!=low)
    {
        high--;
    }
    *low=*high;
    
    while(*low<=num&&low!=high)
    {
        low++;
    }
    *high=*low;

    if(high!=low)
    {
        QukSort(array,low,high,num);
    }
    else *high=num;

    if(tmp_low!=high)
        QukSort(array,tmp_low,high-1,*tmp_low);
    if(tmp_high!=low)
        QukSort(array,low+1,tmp_high,*(low+1));
}
int main()
{
    int array[N]={7,1,7,4,5,2,6,8,10,9};
    int *low=&array[0],*high=&array[N-1];
    QukSort(array,low,high,array[0]);
    for(int i=0;i<N;i++)
        printf("%d ",array[i]);
    return 0;
}