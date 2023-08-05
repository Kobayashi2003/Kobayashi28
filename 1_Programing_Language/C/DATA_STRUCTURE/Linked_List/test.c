#include<stdio.h>
#include<malloc.h>
#define N 10
#define LEN (sizeof(Node))
typedef struct Node
{
    int data;
    int count;
    struct Node *next;
}Node;

int countNode(Node *head)
{
    int count=0;
    Node *p=head->next;
    while(p!=NULL)
    {
        count++;
        p=p->next;
    }
    return count;
}

void creatNode(Node *head,Node *node,int data)
{
    Node *newNode=(Node*)malloc(LEN);
    newNode->next=NULL;
    newNode->data=data;
    node->next=newNode;
    newNode->count=countNode(head);
}

Node* findTail(Node *head)
{
    Node *find=head;
    while(find->next!=NULL)
    find=find->next;
    return find;
}

int HashFaction(int key)
{
    int value;
    //哈希函数 可后期自定义
    value=key%10;
    return value;
}

void creatHashTable(Node **Table,int *data,int n)
{
    for(int i=0;i<N;i++)
    {
        Table[i]=(Node*)malloc(LEN);
        Table[i]->next=NULL;
    }
    for(int i=0;i<n;i++)
    {
        int value=HashFaction(data[i]);
        creatNode(Table[value],findTail(Table[value]),data[i]);
    }
}

void travelTable(Node **Table)
{
    for(int i=0;i<N;i++)
    {
        Node *p=Table[i]->next;
        while(p!=NULL)
        {
            printf("group:%d count:%d data:%d\n",i,p->count,p->data);
            p=p->next;
        }
    }
}

int main()
{
    int data[N]={0};
    int n;
    scanf("%d",&n);
    for(int i=0;i<n;i++)
        scanf("%d",&data[i]);

    Node *Table[N]={NULL};
    creatHashTable(Table,data,n);
    travelTable(Table);

    return 0;
}