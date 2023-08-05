#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))
#define N 5
#define Ture 1
#define Fause 0

typedef struct Node//创建链表结点的结构体
{
    int num;
    char name[N];
    struct Node *next;
}Node;

void createNode(Node *head,int n)//创建链表
{
    Node *tail=head;
    for(int i=0;i<n;i++)
    {
        Node *newNode=(Node*)malloc(LEN);
        newNode->next=NULL;
        printf("Please enter the job number of the staff:\n");
        scanf("%d",&newNode->num);
        printf("Please enter the name of the staff:\n");
        scanf("%s",newNode->name);
        tail->next=newNode;
        tail=newNode;
    }
}

void travelLink(Node *head)//遍历并输出链表
{
    Node *p=head->next;
    while(p!=NULL)
    {
        printf("Job number:%d Staff name:%s\n",p->num,p->name);
        p=p->next;
    }
}

void checkLink(Node* head,int num)//检查链表中所有拥有num值的结点
{
    Node *p=head->next;
    int count=0;
    while(p!=NULL)
    {
        count++;
        if(p->num==num)printf("The staff whose job number is %d is in the %d node\n",num,count);
        p=p->next;
    } 
}

void isFree(Node *head)//判断链表是否为空
{
    Node *p=head->next;
    if(p==NULL)printf("The Link is empty\n");
    else printf("The Link isn't empty\n");
}

int checkNodes(Node *head,int num)//判断链表中是否存在有储存num值的结点
{
    Node *p=head->next;
    while(p!=NULL)
    {
        if(p->num==num)return Ture;
        p=p->next;
    }
    return Fause;
}

void deleteNode(Node *head,int num)//删除拥有num值的(一个)结点
{
    Node *p_det=head->next;
    Node *p=head;
    switch(checkNodes(head,num))
    {
        case Ture:
        while(p_det->num!=num&&p_det->next!=NULL)//BUG1:在找不到对应的num时总是删除链表中的最后一个结点
            p_det=p_det->next;
        while(p->next!=p_det&&p!=NULL)
            p=p->next;
        p->next=p_det->next;
        free(p_det);
        break;
        case Fause:
        printf("There is no the staff whose job number is %d\n",num);
        break;
    }
}

void insertForward(Node *head,int n)//链表前插
{
    Node *p=head,*p_tmp=head->next;
    for(int i=0;i<n;i++)
    {
        Node *insert=(Node*)malloc(LEN);

        if(i==n-1)
            insert->next=p_tmp;
        else
            insert->next=NULL;

        printf("Please enter the job number of the staff:\n");
        scanf("%d",&insert->num);
        printf("Please enter the name of the staff:\n");
        scanf("%s",insert->name);

        p->next=insert;
        p=insert;
    }
}

void insertBack(Node *head,int n)//链表后插
{
    Node *p=head->next;
    while(p->next!=NULL)p=p->next;
    for(int i=0;i<n;i++)
    {
        Node *insert=(Node*)malloc(LEN);
        insert->next=NULL;

        printf("Please enter the job number of the staff:\n");
        scanf("%d",&insert->num);
        printf("Please enter the name of the staff:\n");
        scanf("%s",insert->name);
        
        p->next=insert;
        p=insert;
    }
}

Node* reverseLink(Node *head)//指针翻转(用三个指针进行翻转)
{
    Node *p1=NULL,*p2=head->next,*p3=head->next->next;
    while(p3!=NULL)
    {
        Node *p_tmp=p3->next;
        p2->next=p1;
        p3->next=p2;
        p1=p2;
        p2=p3;
        if(p_tmp==NULL)break;
        else p3=p_tmp;
    }
    free(head);
    Node *newHead=(Node*)malloc(LEN);
    newHead->next=p3;
    return newHead;
}

void changeNode(Node *head,int num1,int num2)//结点交换
{
    Node *p1=head->next,*p2=head->next;
    Node *temp1,*temp2;
    Node temp;
    while(p1->num!=num1&&p1->next!=NULL)p1=p1->next;
    while(p2->num!=num2&&p1->next!=NULL)p2=p2->next;
    temp1=p1->next;
    temp2=p2->next;

    temp=*p1;
    *p1=*p2;
    *p2=temp;

    p1->next=temp1;
    p2->next=temp2;
}

void deletRepeat(Node *head)
{
    
}

int main()
{
    Node *head=(Node*)malloc(LEN);//创建头节点

    int n;
    printf("Please enter the number of the Nodes:\n");
    scanf("%d",&n);

    createNode(head,n);
    travelLink(head);

    int num;
    printf("Please enter the job number of the guy you want to delete:\n");
    scanf("%d",&num);
    deleteNode(head,num);
    travelLink(head);
    isFree(head);

    int n_insert_forward;
    printf("Please enter the number of Nodes you want to insert(forward):\n");
    scanf("%d",&n_insert_forward);
    insertForward(head,n_insert_forward);
    travelLink(head);

    int n_insert_back;
    printf("Please enter the number of Nodes you want to insert(back):\n");
    scanf("%d",&n_insert_back);
    insertBack(head,n_insert_back);
    travelLink(head);

    int num1,num2;
    printf("Please enter the job number of the two staffs you want to change:\n");
    scanf("%d%d",&num1,&num2);
    changeNode(head,num1,num2);
    travelLink(head);

    printf("Reverse the Link:\n");
    head=reverseLink(head);
    travelLink(head);

    return 0;
}
