#include<stdio.h>
#define N 500
int main()
{
    int array[]={},len=sizeof(array)/sizeof(int);
    int i;
    int Table[N][2]={0};
    int num=0;
    Table[num][0]=array[0];
    for(i=1;i<len;i++)
    {
        if(array[i]==Table[num][0])Table[num][1]++;
        else 
        {
            num++;
            Table[num][0]=array[i];
        }
    }
    printf("%d\n",num+1);
    for(i=0;i<num+1;i++)
    {
        printf("%d,",Table[i][0]);
    }
    printf("\n\n");
    for(i=0;i<num+1;i++)
    {
        printf("%d,",Table[i][1]);
    }
    printf("\n\n");
    return 0;
}