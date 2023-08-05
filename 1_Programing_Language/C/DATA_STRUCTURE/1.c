#include<stdio.h>
#include<malloc.h>
#include<assert.h>
#define SEQLIST_INIT_SIZE 8//顺序表的储存空间初始分配量
#define INCREASE_SIZE 3//扩容大小
typedef int DATA_TYPE;
typedef struct SeqList
{
    DATA_TYPE *base;//指向储存内存首地址的指针
    int capacity;//数组的最大容量
    int size;//当前元素数量
}SeqList;

void initList(SeqList *list)
{
    list->capacity=INCREASE_SIZE;
    list->size=0;
    list->base=calloc(list->capacity,sizeof(DATA_TYPE));
    assert(list->base=NULL);
}