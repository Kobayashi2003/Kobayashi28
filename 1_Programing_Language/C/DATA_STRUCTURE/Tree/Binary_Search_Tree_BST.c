//二叉排序树
#include<stdio.h>
#include<malloc.h>
#define LEN (sizeof(Node))
typedef int DATA;
char *format="%-3d";
typedef struct Node//树结点
{
    DATA value;
    struct Node *left;
    struct Node *right;
}Node;

typedef struct
{
    Node *root;//树的根结点
}Root;
void insertTree(Root *tree,DATA value)
{
    Node *newNode=(Node*)malloc(LEN);
    newNode->value=value;
    newNode->left=NULL;
    newNode->right=NULL;
    if(tree->root==NULL)tree->root=newNode;
    else
    {
        Node *temp=tree->root;
        while(temp!=NULL)
        {
            if(value>temp->value)
            {
                if(temp->left==NULL) 
                {
                    temp->left=newNode;
                    return;
                }
                else temp=temp->left;
            }
            else
            {
                if(temp->right==NULL)
                {
                    temp->right=newNode;
                    return;
                }
                else temp=temp->right;
            } 
        }
    }
}
void travelTree(Node *node)
{
    if(node!=NULL)
    {
        travelTree(node->right);
        printf(format,node->value);
        travelTree(node->left);
    }
}
void distoryTree(Node *node)
{
    if(node!=NULL)
    {
        distoryTree(node->left);
        distoryTree(node->right);
        printf("Distory:%d\n",node->value);
        free(node);
        node=NULL;
    }
}
int main()
{
    Root tree;
    tree.root=NULL;//创造一颗空树,此时根结点悬空不指向任何地址
    DATA value[]={3,1,2};
    int len=sizeof(value)/sizeof(DATA);
    for(int i=0;i<len;i++)
        insertTree(&tree,value[i]);
    travelTree(tree.root);
    putchar('\n');
    distoryTree(tree.root);
    return 0;
}