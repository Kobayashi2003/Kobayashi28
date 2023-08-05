#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(NODE))
typedef struct NODE
{
    int num;
    struct NODE *next;
}NODE;
void createNode(NODE *ent,int n)
{
    NODE *tmp=ent;
    tmp->next=NULL;
    for(int i=0;i<n;i++)
    {
        NODE *newnode=(NODE*)malloc(LEN);
        newnode->num=i+1;
        newnode->next=NULL;
        tmp->next=newnode;
        tmp=newnode;
    }
    tmp->next=ent->next;
}
void deleteNode(NODE *node)
{
    NODE *tmp=node->next->next;
    free(node->next);
    node->next=tmp;
}
void travelNode(NODE *ent)
{
    int cont=0;
    NODE *p=ent;
    while(p->next!=p)
    {
        cont++;
        p=p->next;
        if(cont%3==2)
        {
            deleteNode(p);
            cont++;
        }
    }
    printf("The last player is:%d\n",p->num);
}
int main()
{
    int n;
    NODE *enterence=(NODE*)malloc(LEN);
    printf("Please enter the number of the players:");
    scanf("%d",&n);
    createNode(enterence,n);
    travelNode(enterence);
    return 0;
}