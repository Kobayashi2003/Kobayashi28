//拉链法 解决哈希冲突 数组内储存的是指针
#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))
#define N 10
#define N2 10
#define Ture 1
#define False 0
typedef struct Node
{
    int data;
    struct Node *next;
}Node;

void createNode(Node *head,int data)
{
    Node *newNode=(Node*)malloc(sizeof(Node));
    newNode->next=NULL;
    newNode->data=data;
    head->next=newNode;
}

Node* findBottomNode(Node *head)
{
    Node *p=head;
    while(p->next!=NULL)p=p->next;
    return p;
}

int HashFunction(int key)
{
    int value;
    value=key%10;
    return value;
}

int travelTable(Node *hashTable[],int num)
{
    Node *p=hashTable[HashFunction(num)]->next;
    while(p!=NULL)
    {
        if(p->data==num)return 1;
        p=p->next;
    }
    return 0;
}

int main()
{
    Node *hashTable[N]={NULL};
    for(int i=0;i<N;i++)
    {
        Node *head=(Node*)malloc(LEN);
        head->data=-1;
        head->next=NULL;
        hashTable[i]=head;
    }

    int data[N2]={1,3,4,5,9,11,15,25,30,31};
    for(int i=0;i<N;i++)
        createNode(findBottomNode(hashTable[HashFunction(data[i])]),data[i]);
    
    int num;
    scanf("%d",&num);
    switch(travelTable(hashTable,num))
    {
        case Ture:
        printf("The num %d is in the hash table\n",num);
        break;
        case False:
        printf("The num %d is not in the hash table\n",num);
        break;
    }

    return 0;
}