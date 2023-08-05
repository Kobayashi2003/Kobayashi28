//ADT tree
//Data 树是由一个根节点和若干棵子树构成。树中结点具有相同数据类型及层次关系
//Operation
//InitTree(*T) 构造空树T
//DestroyTree(*T) 摧毁树T
//CreateTree(*T,definition) 按definition中给出的树的定义来构造树
//ClearTree(*T) 若树T存在，则将树T清空为空树
//TreeEmpty(*T)若树T为空树 返回Ture 否则返回False
//TreeDepth(*T)返回T的深度
//Root(*T)返回树的根节点
//Value(*T,cur_e) cur_e是树T中的一个结点 返回该结点的值
//Assign(*T,cur_e,value) 给树T的结点cur_e赋值为value
//Parent(*T,cur_e) 若cur_e是树T的非根节点 则返回它的双亲 否则为空
//LetfChild(*T) 若cur_e是树T的非叶节点 返回它的左孩子 否则为空
//RightChild(*T) ...
//InsertChild(*T,*p,i,c) 其中p指向树T的某个节点 i为所指的结点p的度加上1 非空树c与T不相交 操作结果为插入c为树T中p指结点的第i棵子树
//DeleteChild(*T,*p,i) 其中p指向树T的某个节点 i为所指结点p的度 操作结果为删除T中p所指结点的第i棵子树

//三种表示法
//双亲表示法 孩子表示法 孩子兄弟表示法


//双亲表示法
#include<stdio.h>
#define MAX_TREE_SIZE 100
typedef int TElemType;//树结点的数据类型

typedef struct PTNode//结点结构
{
    TElemType data;//结点数据
    int parent;//双亲位置
}PTNode;

typedef struct//树结构
{
    PTNode nodes[MAX_TREE_SIZE];//结点数组
    int r,n;//根的位置和结点数
}PTree;



//孩子表示法
#define MAX_TREE_SIZE 100 

typedef struct CTNode//孩子结点
{
    int child;//孩子结点在表头数组中的下标
    struct CTNode *next;//指向某结点的下一个孩子结点
}*ChildPtr;

typedef struct//表头数组
{
    TElemType data;//某结点的数据域，储存某结点的数据信息
    ChildPtr firstchild;//指向某结点的第一个孩子
}CTBox;

typedef struct//树结构
{
    CTBox nodes[MAX_TREE_SIZE];//结点数组
    int r,n;//根的位置和结点数
}CTree;

//孩子兄弟表示法
typedef