#include<stdio.h>
#include<time.h>
#include<stdlib.h>
#include<math.h>
#define N (sizeof(SYMBOL)/sizeof(const char*))
#define MAX_VALUE 10000
#define MIN_VALUE 1
#define TABLE_SIZE 6 
typedef unsigned long long int ULL;
const char *SYMBOL[]={"I","AM","A","STUDENT"};
void QukSort(ULL *low,ULL *high)
{
    ULL middle=*low,*tmp_low=low,*tmp_high=high;
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
    ULL TABLE[N];
    for(int i=0;i<N;i++)
    {
        srand((unsigned)((rand()*time(NULL)-i*(ULL)1e5)&0x8b54c359));
        TABLE[i]=rand()%(MAX_VALUE-MIN_VALUE+1)+MIN_VALUE;
    }
    ULL *low=&TABLE[0],*high=&TABLE[N-1];
    QukSort(low,high);
    for(int i=0;i<N;i++)
    {
        printf("%5d---%-5s ",TABLE[i],SYMBOL[i]);
        if((i+1)%TABLE_SIZE==0||i==N) printf("\n");
    }
    return 0;
}