#include<stdio.h>
#include<malloc.h>
//树结点
typedef struct node
{
    int data;
    struct node *left;//结点左边的树枝
    struct node *right;//结点右边的树枝
}Node;
//树根
typedef struct tree
{
    Node *root;
}Tree;
//根节点也是一个节点，只不过这个结点代表了这棵树

void insert(Tree *tree,int value)
{
    Node *node=(Node*)malloc(sizeof(Node));//创建一个节点
    node->data=value;
    node->left=NULL;
    node->right=NULL;
    //判断该树是不是空树
    if(tree->root==NULL)
    {
        tree->root=node;
    }
    else //该树不是空树
    {
        Node *temp=tree->root;//从树根开始
        while(temp!=NULL)
        {
            if(value<temp->data)//小于就进入左子树中
            {
                if(temp->left==NULL)
                {
                    temp->left=node;
                    return;
                }
                else//继续寻找，直至找到叶结点
                {
                    temp=temp->left;
                }
            }
            else//否则就进右节点
            {
                if(temp->right==NULL)
                {
                    temp->right=node;
                    return;
                }
                else 
                {
                    temp=temp->right;
                }
            }
        } 
    }
}
//遍历一整颗树 中序遍历：先左再右
void traverse(Node *node)
{
    if(node!=NULL)
    {
        traverse(node->left);
        printf("%-3d",node->data);
        traverse(node->right);
    }
}
void distory_tree(Node *node)
{
    if(node!=NULL)
    {
        distory_tree(node->left);
        distory_tree(node->right);
        printf("free node %d\n",node->data);
        free(node);
        node=NULL;
    }
}
int main()
{
    Tree tree;
    tree.root=NULL;//创建一颗空树
    int value[]={10,9,8,2,1,3,4,5,7,6};
    int len=sizeof(value)/sizeof(int);
    for(int i=0;i<len;i++)
    {
        insert(&tree,value[i]);
    }
    traverse(tree.root);
    putchar('\n');
    distory_tree(tree.root);
    return 0;
}