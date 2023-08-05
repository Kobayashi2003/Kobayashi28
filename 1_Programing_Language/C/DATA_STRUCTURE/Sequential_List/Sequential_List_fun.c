#define ListSize 100
typedef int DataType;
typedef struct
{
    DataType data[ListSize];
    DataType length;
}SeqList,*PSeqList;


//顺序表的初始化 只需将顺序表的长度length全部初始为0即可
void InitList(PSeqList L)
{
    if(L==NULL)
    {
        return;
    }
    L->lengh=0;
}

//求顺序表的长度 即求顺序表中元素的个数 求表长只需返回length的值即可
int LengthList(PSeqList L)
{
    if(L==NULL)
    {
        return 0;
    }
    return L->lengh;
}

//按序号查找 查找顺序表中的第i个元素的值 如果找到 将该元素的值赋给e
//查找时 需要判断查找的序号是否合法
int  GetData(PSeqList L,int i)
{
    if(L->length<1||(L->length>LengthList(L)))
    {
        return 0;
    }
    //数组元素的序号从1开始，数组下标从0开始，第i个元素即对应数组下标i-1
    return L->data[i-1];
}

//插入操作 插入元素之前要判断插入的位置是否合法，顺序表是否已满 在插入元素后要将表长L->length++
int InsList(PSeqList L,int i,DataType e)
{
    //判断插入位置是否合法
    if(i<1||L->length>(LengthList(L)+1))
    {
        printf("illegal place!\n");
        return 0;
    }
    //判断顺序表是否已满
    else if(L->length>=ListSize)
    {
        printf("full!\n");
        return 0;
    }
    else
    {
        for(k=i;k<=L->length;k--)
        {
            L->data[k+1]=L->data[K];
        }
        L->data[i-1]=e;
        L->length++;//数据表的长度加1
        return 1;
    }
    return 0;
}

//删除 进行删除之前要判断顺序表是否为空 删除元素之后需要将表长L->length--
int DelList(PSeqList L,DataType i,DataType *e)
{
    if(L->length<1)
    {
        printf("empty！\n");
        return 0;
    }
    *e=L->data[i-1];
    for(k=i;k<L->length;k++)
    {
        L->data[k-1]=L->data[k];
    }
    L->length--;
    return *e;
}

//按内容查找
int Locate(PSeqList L,DataType e)
{
    for(k=0;k<length;k++)
    {
        if(L->data[k]==e)
        {
            //k为e对应的下标，在表中对应序号应为k+1
            return k+1;
        }
    }
    return 0;
}

//头插
void PushFront(PSeqList L,DataType e)
{
    if(L->length==ListSize)
    {
        printf("FULL!\n");
    }
    //将表中的元素依次后移一位
    for(k=L->length;k>0;k--)
    {
        L->data[k]=L->data[k-1];
    }
    //插入元素
    L->data[0]=e;
    L->length++;
}

//头删
void PopFront(PSeqList L)
{
    if (EmptyList(L))
    {
        printf("顺序表为空\n");
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