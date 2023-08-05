//结构体实现
#include<stdio.h>
#define N 3
#define LEN 10
typedef struct Staff  
{
    int num;
    char name[LEN];
}Staff;
void Sort(Staff *staff)
{
    for(int start=0;start<N-1;start++)
        for(int i=start;i<N;i++)
            if(staff[i].num<staff[start].num)
            {
                Staff temp=staff[start];
                staff[start]=staff[i];
                staff[i]=temp;
            }
}
int main()
{
    Staff staff[N];
    for(int i=0;i<N;i++)
    {
        printf("Please enter the jop number of the %d staff:\n",i+1);
        scanf("%d",&staff[i].num);
        printf("Please enter the name of the %d staff:\n",i+1);
        scanf("%s",staff[i].name);
    }
    Sort(staff);
    for(int i=0;i<N;i++)
        printf("the job number:%d\nthe name:%s\n",staff[i].num,staff[i].name);
    return 0;
}