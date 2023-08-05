#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))
typedef int DATA;
char *format="%d\n";
typedef struct Node
{
    DATA data;
    struct Node *next;
}Node;
void createLink(Node *entry,DATA *data,int len)
{
    entry->data=data[0];
    Node *tmp=entry;
    for(int i=1;i<len;i++)
    {
        Node *newNode=(Node*)malloc(LEN);
        newNode->data=data[i];
        newNode->next=NULL;
        tmp->next=newNode;
        tmp=newNode;
    }
    tmp->next=entry;
}
void travelLink(Node *entry,int n)
{
    Node *p=entry;
    while(1)
    {
        if(p==entry)n--;
        if(n+1==0)break;
        printf(format,p->data);
        p=p->next;
    }
}
int main()
{
    Node *entry=(Node*)malloc(LEN);
    DATA data[]={1,2,3,4,5};
    int len=sizeof(data)/sizeof(DATA);
    createLink(entry,data,len);
    travelLink(entry,3);
    return 0;
}