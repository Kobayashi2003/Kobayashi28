//关于realloc的使用 https://www.cnblogs.com/a155-/p/12002677.html
#include<stdio.h>
#include<malloc.h>
#define N 10
typedef int DATA_TYPE;
typedef struct SeqList
{
    DATA_TYPE *data;
    int size;//有效数据个数
    int capisity;//数组的容量
}SeqList,*PSeqList;
int main()
{
    SeqList table;
    table.data=(DATA_TYPE*)malloc(N*sizeof(DATA_TYPE));
    table.size=0;
    table.capisity=N;
    DATA_TYPE data[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21};
    for(int i=0;i<sizeof(data)/sizeof(DATA_TYPE);i++)
    {
        if(table.size==table.capisity)
        {
            table.data=(DATA_TYPE*)realloc(table.data,2*table.capisity*sizeof(DATA_TYPE));
            table.capisity*=2;
        }
        table.data[table.size++]=data[i];
    }
    for(int i=0;i<table.size;i++)
    {
        printf("%d ",table.data[i]);
    }
    printf("\n");
    return 0;
}