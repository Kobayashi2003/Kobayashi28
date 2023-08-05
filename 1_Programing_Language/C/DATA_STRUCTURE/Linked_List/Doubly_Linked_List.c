//双向链表的创建
#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))
typedef char DATA;
char *Format="the data is: %c\n";
typedef struct Node
{
    DATA data;
    struct Node *left;
    struct Node *right;
}Node;
void createNode_left(Node *leftHead,DATA data)//通过左头结点插入新结点
{
    Node *temp=leftHead->right;
    Node *newNode=(Node*)malloc(LEN);

    newNode->data=data;//输入数据

    newNode->left=leftHead;//双向连接新结点与左头结点
    leftHead->right=newNode;

    newNode->right=temp;//双向连接新结点与原位于左头结点右端的结点
    temp->left=newNode;
}
void createNode_right(Node *rightHead,DATA data)//通过右头结点插入新结点
{
    Node *temp=rightHead->left;
    Node *newNode=(Node*)malloc(LEN);

    newNode->data=data;

    newNode->right=rightHead;//双向连接新结点与右头结点
    rightHead->left=newNode;

    newNode->left=temp;//双向连接新结点与原位于右头结点左端的结点
    temp->right=newNode;
}
void travelLink_left(Node *leftHead,Node *rightHead)//由左向右遍历链表
{
    Node *p=leftHead->right;
    while(p!=rightHead)
    {
        printf(Format,p->data);
        p=p->right;
    }
}
void travelLink_right(Node *rightHead,Node *leftHead)//由右向左遍历链表
{
    Node *p=rightHead->left;
    while(p!=leftHead)
    {
        printf(Format,p->data);
        p=p->left;
    }
}
int main()
{
    Node *leftHead=(Node*)malloc(LEN),*rightHead=(Node*)malloc(LEN);
    leftHead->right=rightHead;
    leftHead->left=NULL;
    rightHead->left=leftHead;
    rightHead->right=NULL;

    DATA data[]="abcde";
    int Len=sizeof(data)/sizeof(DATA);

    for(int i=0;i<Len;i++)
    {
        createNode_left(leftHead,data[i]);
    }

    travelLink_left(leftHead,rightHead);
    printf("\n\n");
    travelLink_right(rightHead,leftHead);

    return 0;
}