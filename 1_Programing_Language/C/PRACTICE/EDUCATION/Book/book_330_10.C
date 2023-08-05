#include <stdio.h>
#include <malloc.h>
#define LEN1 (sizeof(NODE))
#define LEN2 (sizeof(TreeNode))
typedef struct NODE //链表结点
{
    int num;
    struct NODE *next;
} NODE;

typedef struct BST // BST树结点
{
    NODE *save;
    struct BST *lchild, *rchild;
} TreeNode, ROOT;

NODE *bridge = NULL;

void createNode(NODE *head, int *value, int n) //创造一个属于链表的结点
{
    NODE *tmp = head;
    for (int i = 0; i < n; i++)
    {
        NODE *newNode = (NODE *)malloc(LEN1);
        newNode->num = value[i];
        newNode->next = NULL;
        tmp->next = newNode;
        tmp = newNode;
    }
}

void connectLinks(NODE *head1, NODE *head2) //连接两张链表
{
    NODE *tmp = head1;
    while (tmp->next != NULL)
    {
        tmp = tmp->next;
    }
    tmp->next = head2->next;
}

TreeNode *createTreeNode(NODE *data) //创造树结点
{
    TreeNode *newNode = (TreeNode *)malloc(LEN2);
    newNode->save = data;
    newNode->lchild = NULL;
    newNode->rchild = NULL;
    return newNode;
}

TreeNode *createTree(TreeNode *root, NODE *head) //创造BST树
{
    NODE *tmp = head->next;
    while (tmp != NULL)
    {
        if (root == NULL)
        {
            root = createTreeNode(tmp);
            tmp = tmp->next;
        }
        else
        {
            TreeNode *p = root;
            while (p != NULL)
            {
                if (tmp->num > p->save->num) //将较大的数放在左子树中
                {
                    if (p->lchild == NULL)
                    {
                        p->lchild = createTreeNode(tmp);
                        tmp = tmp->next;
                        break;
                    }
                    else
                    {
                        p = p->lchild;
                    }
                }
                else //将较小的的数放在右子树中
                {
                    if (p->rchild == NULL)
                    {
                        p->rchild = createTreeNode(tmp);
                        tmp = tmp->next;
                        break;
                    }
                    else
                    {
                        p = p->rchild;
                    }
                }
            }
        }
    }
    return root;
}

void travelTree_and_connectNodes(TreeNode *node) //遍历BST树，并将结点排序后进行重新连接
{
    if (node != NULL)
    {
        travelTree_and_connectNodes(node->rchild);
        node->save->next = bridge;
        bridge = node->save;
        travelTree_and_connectNodes(node->lchild);
    }
}

void travelLink(NODE *head) //遍历链表
{
    NODE *p = head->next;
    while (p != NULL)
    {
        printf("the number is:%d\n", p->num);
        p = p->next;
    }
}

int main()
{
    //首先创建两张链表
    NODE *head1 = (NODE *)malloc(LEN1);
    NODE *head2 = (NODE *)malloc(LEN1);
    head1->next = NULL;
    head2->next = NULL;
    int Value1[] = {3, 2, 1};
    int Value2[] = {6, 5, 4, 7};
    createNode(head1, Value1, sizeof(Value1) / sizeof(int));
    createNode(head2, Value2, sizeof(Value2) / sizeof(int));

    travelLink(head1);
    putchar('\n');
    travelLink(head2);
    putchar('\n');

    connectLinks(head1, head2);

    ROOT *root = createTree(NULL, head1);
    travelTree_and_connectNodes(root);

    head1->next = bridge;
    travelLink(head1);

    return 0;
}