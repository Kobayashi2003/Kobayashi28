//创造一个链表，令其储存n个value值,并通过遍历链表的形式将储存的值输出
#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))//定义每次开辟的储存空间的大小
typedef struct Node//定义链表结点的结构体
{
    int value;//定义value，用于储存数据
    struct Node *next;
}Node;

void createLink(Node *head)
{
    printf("Please enter the number you want to store:\n");
    Node *rear=head;
    for(int i=0;i<head->value;i++)//将头结点中所储存的数据记为非头结点的数量
    {
        Node *newNode=(Node *)malloc(LEN);//开辟新的储存空间，即为创造新的结点
        newNode->next=NULL;//令下一结点的next指针悬空
        scanf("%d",&newNode->value);//将需要储存的数据储存到该结点中
        rear->next=newNode;//令当前节点中的next指针指向下一结点
        rear=newNode;
    }
}

void travelLink(Node *head)//遍历结点，将储存的数据输出
{
    Node *p=head->next;
    printf("Travel the numbers:\n");
    while(p!=NULL)
    {
        printf("%d ",p->value);
        p=p->next;
    }
}

int main()
{
    Node *head=malloc(LEN);//定义头节点
    printf("Please input the number of nodes you want to creat:\n");
    scanf("%d",&head->value);
    createLink(head);
    travelLink(head);
    return 0;
}