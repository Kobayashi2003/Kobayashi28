#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef int ElementType;// typedef在C语言中可用来为数据类型定义别名
//typedef double ElementType;
typedef struct LNode* List;   
struct LNode{
    ElementType data; // 此处等价于int Data；
    List next;
};

/*基本操作集*/
List makeEmpty();//初始化一个空的链表，生成仅含第0个节点为头空结点的空链表
List findKth (int k, List ptrL);//根据位序k，返回相应结点指针，k的范围[0,length(ptrL)]
List findX(ElementType X, List ptrL);//链表ptrL中查找X的第一次出现的结点指针
bool deleteKth(int k, List ptrL); //删除指定位序k的结点,k的范围[1,length(ptrL)]
bool insert(ElementType X, int k, List ptrL); //在位序k前插入一个新结点，使新结点在位序k, k的范围[1,length(ptrL)+1]
int length(List L);//返回线性表L的长度n，头空结点不计入长度

/*其他操作（可由基本操作集实现）*/
List createLink(int n, ElementType* arr); // 将arr数组中的n个数按位序从小到大顺序创建链表
void destroyLink(List ptrL);//销毁链表，释放内存
void printLink(List ptrL);//按从头至尾的顺序输出链表每个节点的val值
bool deleteKthEnd(int k, List ptrL);



bool deleteKthEnd(int k, List ptrL)
{
    List p = ptrL;
    List q = ptrL;
    int i = 0;
    int n = length(ptrL);
    if(k < 1 || k > n)
        return false;
    while(i < k)
    {
        p = p->next;
        ++i;
    }
    while(p->next != NULL)
    {
        p = p->next;
        q = q->next;
    }
    List s = q->next;
    q->next = s->next;
    free(s);
    return true;
}


bool insert(ElementType X, int k, List ptrL)
{
    List p = ptrL;
    int i = 0;
    int n = length(ptrL);
    if(k < 1 || k > n+1)
        return false;
    while(i < k-1)
    {
        p = p->next;
        ++i;
    }
    List s = (List)malloc(sizeof(struct LNode));
    s->data = X;
    s->next = p->next;
    p->next = s;
    return true;
}


bool deleteKth(int k, List ptrL)
{
    List p = ptrL;
    int i = 0;
    int n = length(ptrL);
    if(k < 1 || k > n)
        return false;
    while(i < k-1)
    {
        p = p->next;
        ++i;
    }
    List s = p->next;
    p->next = s->next;
    free(s);
    return true;
}


/*基本操作集*/

/*初始化一个空的链表，第0个节点为空节点*/
List makeEmpty(){
    List L;
    L = (List)malloc(sizeof(struct LNode));
    L->next = NULL;
    return L;
}
/*按位序查找，根据位序K，返回相应结点指针,有效值为[0,length(ptrL)]*/
List findKth (int k, List ptrL){
    List p = ptrL;
    int i = 0;
    //int n = length(List);
    if(k < 0 || k > length(ptrL)){//k 的有效值为[0,length(ptrL)]
		return NULL;
    }
	if(k == 0)
		return ptrL;
	while(p->next != NULL)
    {
        p = p->next;
        ++i;
        if(i==k)
        	return p;
    }
    return NULL;
}
/*按值查找，在链表ptrL中查找X的第一次的结点指针*/
List findX(ElementType X, List ptrL)
{
	int i = 0;
	List p;
	p = ptrL;
	while(p->next != NULL)
	{
		p = p->next;
		++i;
		if(p->data == X)
			return p;
	}	
	return NULL;//链表L中未出现X
}
/*返回线性表L的长度n*/
int length(List ptrL)//只有头结点的链表为空
{
	int i = 0;
	List p;
	p = ptrL;
	while(p->next != NULL)
	{
		p = p->next;
		++i;
	}
	return i;
}

/*其他操作（可由基本操作集实现）*/

/*将arr数组中的n个数按位序从小到大创建链表*/
List createLink(int n, ElementType* arr)
{
	List L = makeEmpty();//创建空链表
	int i;
	List p = L;
	for(i = 0; i < n; i++)
	{
		List s = (List)malloc(sizeof(struct LNode));
		s->data = arr[i];
		s->next = NULL;
		p->next = s;
		p = s;
	}
	return L;
}

/*销毁链表，释放内存*/
void destroyLink(List ptrL)
{
	List p = ptrL;
	List s = p->next;
	while(s != NULL){
		free(p);
		p = s;
		s = s->next;	
	}
	free(p);
}

/*按从头至尾的顺序输出链表每个结点的data值*/
void printLink(List ptrL)
{
	List p = ptrL;
	int n = length(ptrL);
	while(n--)
	{
		p = p->next;
		printf("%d ", p->data);	
	}
}

int main()
{
    int n,k;
    scanf("%d%d",&n,&k);
    int* arr = (int*) malloc(sizeof(int)*n);
    int i;
    for(i = 0; i < n; i++)
    {
        scanf("%d",arr+i);
    }
    List ptrL = createLink(n,arr);
    deleteKthEnd(k,ptrL);
    printLink(ptrL);
    free(arr);
    destroyLink(ptrL);
    return 0;
}