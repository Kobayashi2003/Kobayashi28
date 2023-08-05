#include <stdio.h>
#include <Windows.h>

#define ListSize 100      //线性表的最大长度
typedef int DataType;

typedef struct
{
    DataType data[ListSize];   //用数组存储线性表中的元素
    DataType length;           //顺序表的长度
}SeqList, *PSeqList;

int k = 0;  //全局变量，用于作部分操作的循环变量

//初始化顺序表
void InitList(PSeqList L)
{
    if (L == NULL)
    {
        return;
    }
    L->length = 0;
}

//求顺序表的长度

int LengthList(PSeqList L)
{
    if (L == NULL)
    {
        return 0;
    }
    return L->length;
}

//返回数据表中第i个元素的值
int GetData(PSeqList L, int i)
{
    if (L->length < 1 || (L->length > LengthList(L)))
    {
        return 0;
    }
    //数据元素的序号从1开始，数组下表从0开始，第i个元素对应的数组下标为i-1;
    return L->data[i - 1];
}

//在L中第i个位置，插入新的数据元素e

int InsList(PSeqList L, int i, DataType e)
{

    //判断插入位置是否合法
    if (i < 1 || L->length >(LengthList(L) + 1))
    {
        printf("插入位置不合法!\n");
        return 0;
    }
    //判断顺序表是否已满
    else if (L->length >= ListSize)
    {
        printf("顺序表已满，不能插入！\n");
        return 0;
    }
    else
    {
        for (k = i; k <= L->length; k--)
        {
            L->data[k + 1] = L->data[k];
        }
        L->data[i - 1] = e;
        L->length++;   //数据表的长度加1
        return 1;
    }
    return 0;
}

//删除L的第i个数据元素

int DelList(PSeqList L, DataType i, DataType* e)
{
    if (L->length < 1)
    {
        printf("表为空！\n");
        return  0;
    }
    *e = L->data[i - 1];
    for (k = i; k < L->length; k++)
    {
        L->data[k - 1] = L->data[k];
    }
    L->length--;
    return *e;
}

//查找e在表中的位置

int Locate(PSeqList L, DataType e)
{
    for (k = 0; k < L->length; k++)
    {
        if (L->data[k] == e)
        {
            //k为e对应的数组下标，在表中对应序号应为k+1
            return k + 1;
        }
    }
    return 0;
}

//头插，在表头插入元素e

void PushFront(PSeqList L, DataType e)
{
    if (L->length == ListSize)
    {
        printf("顺序表已满，不能插入！\n");
    }
    //将表中元素依次后移一位
    for (k = L->length; k > 0; k--)
    {
        L->data[k] = L->data[k - 1];
    }
    //插入元素
    L->data[0] = e;
    L->length++;
}

//头删,删除顺序表中的第一个元素，把顺序表中的元素依次往前移动一位

void PopFront(PSeqList L)
{
    if (EmptyList(L))
    {
        printf("顺序表为空，不能插入！\n");
    }
    for (k = 1; k <= L->length - 1; k++)
    {
        L->data[k - 1] = L->data[k];
    }
    L->length--;
}

//尾插
void PushBack(PSeqList L, DataType e)
{
    if (L->length == ListSize)
    {
        printf("顺序表已满，不能插入!\n");
    }
    L->data[L->length] = e;
    L->length++;
}


//尾删
void PopBack(PSeqList L)
{
    if (EmptyList(L))
    {
        printf("表为空！\n");
    }
    L->length--;

}

//清空顺序表
void ClearList(PSeqList L)
{
    L->length = 0;
}

//判断表是否为空

int EmptyList(PSeqList L)
{
    if (L->length == 0)
    {
        return 1;
    }
    return 0;
}

//打印表中元素

void PrintList(PSeqList L)
{
    if (EmptyList(L))
    {
        printf("表为空！\n");
        return;
    }
    for (k = 0; k < L->length; k++)
    {
        printf("%-3d", L->data[k]);
    }
    printf("\n");
}

int main()
{
    SeqList L;
    DataType data;
    //初始化顺序表
    InitList(&L);
    //在表中插入元素
    printf("依次在表中插入元素(1,2,3,4,5)：\n");
    InsList(&L, 1, 1);
    InsList(&L, 2, 2);
    InsList(&L, 3, 3);
    InsList(&L, 4, 4);
    InsList(&L, 5, 5);

    //打印表中元素
    printf("表中元素有：\n");
    PrintList(&L);
    //头插
    printf("在表头依次插入元素，6,7:\n");
    PushFront(&L, 6);
    PushFront(&L, 7);
    //尾插
    printf("在表尾依次插入元素，8,9:\n");
    PushBack(&L, 8);
    PushBack(&L, 9);
    printf("表中元素有：\n");
    PrintList(&L);
    //头删
    printf("头删一个元素:\n");
    PopFront(&L);
    //尾删
    printf("尾删一个元素:\n");
    PopBack(&L);
    //输出表中第4个元素值
    PrintList(&L);
    printf("表中第4个元素值为：\n%d\n",GetData(&L, 4));
    //查找表中第 i个元素的位置
    printf("元素2在表中的位置为：\n");
    printf("%d\n",Locate(&L, 2));
    //删除表中第2个元素对应的值
    printf("删除表中第2个元素：%d\n", DelList(&L, 2, &data));
    printf("顺序表的长度为：%d\n", LengthList(&L));
    printf("表中元素为：\n");
    PrintList(&L);
    //printf("删除的元素值为：%d\n", data);
    //清空顺序表
    ClearList(&L);
    PrintList(&L);
    system("pause");
    return 0;
}