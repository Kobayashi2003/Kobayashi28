#include<stdio.h>
#define N 11
int array[N]={92,99,80,95,100,95,100,100,99,100};
void QukSort(int *low,int *high)
{
    int middle=*low,*tmp_low=low,*tmp_high=high;
    for (;;)
    {
        while(*high>=middle&&high!=low) high--;
        *low=*high;
        while(*low<=middle&&low!=high) low++;
        *high=*low;
        if(low==high)
        {
            *low=middle;
            break;
        }
    }
    if(tmp_low!=low) QukSort(tmp_low,low-1);
    if(tmp_high!=high) QukSort(high+1,tmp_high);
}
int main()
{
    int *low=&array[0],*high=&array[N-1];
    QukSort(low,high);
    for(int i=0;i<N;i++)
        printf("%d ",array[i]);
    return 0;
}