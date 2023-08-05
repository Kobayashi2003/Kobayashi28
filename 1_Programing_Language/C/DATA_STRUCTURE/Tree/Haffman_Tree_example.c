#include<stdio.h>
#define MAXVALUE 32767
typedef struct{      //哈夫曼树结构体
    int weight;                       //输入权值
    int parent,lchild,rchild;        //双亲节点，左孩子，右孩子
}HNodeType;

typedef struct{     //哈夫曼编码结构体
    int bit[8];     //存放当前结点的哈夫曼编码
    int start;      //bit[start]-bit[8]存放哈夫曼编码
}HCodeType;

HNodeType HuffNode[8];  //定义全局变量数组HuffNode存放哈夫曼树
HCodeType HuffCode[8];  //定义全局变量数组HuffCode存放哈夫曼编码
int n;       //定义全局变量n表示叶子结点个数

/*
*   void CreateHuffTree(void);   //构造哈夫曼树
*   void PrintHuffTree(void);   //输出哈夫曼树
*   void CreateHuffCode(void);   //构造哈夫曼编码
*   void PrintHuffcode(void);   //输出每个叶子结点的哈夫曼编码
*/

void CreateHuffTree(void){  //构造哈夫曼树
    int i,j,a,b,x1,x2;
    scanf("%d",&n);        //输入叶子节点个数
    
    for(i=1;i<2*n;i++) //HuffNode 初始化 
    {
        HuffNode[i].weight=0;
        HuffNode[i].parent=-1;
        HuffNode[i].lchild=-1;
        HuffNode[i].rchild=-1;
    }

    printf("输入%d个节点的权值\n",n);
    for(i=1;i<=n;i++)
        scanf("%d",& HuffNode[i].weight);//输入N个叶子节点的权值

    for(i=1;i<n;i++){   //构造哈夫曼树 
        a=MAXVALUE;
        b=MAXVALUE;
        x1=0;
        x2=0;

        for(j=1;j<n+i;j++){        //选取最小和次小两个权值
            if(HuffNode[j].parent==-1&&HuffNode[j].weight<a){
            b=a;
            x2=x1;
            a=HuffNode[j].weight;
            x1=j;
        }
        else
            if(HuffNode[j].parent==-1&&HuffNode[j].weight<b){
                b=HuffNode[j].weight;
                x2=j;
            }
        }
         
    HuffNode[x1].parent=n+i;
    HuffNode[x2].parent=n+i;
    HuffNode[n+i].weight=HuffNode[x1].weight+HuffNode[x2].weight;
    HuffNode[n+i].lchild=x1;
    HuffNode[n+i].rchild=x2;
    }
}

void PrintHuffTree() {   //输出哈夫曼树
    int i;
    printf("\n哈夫曼树各项数据如下表所示:\n");
    printf("        结点i weight parent    lchid    rchild\n");
    for(i=1;i<2*n;i++)
        printf("\t%d\t%d\t%d\t%d\t%d\n",i,HuffNode[i].weight,HuffNode[i].parent,HuffNode[i].lchild,HuffNode[i].rchild);
    printf("\n");
}

void CreateHuffCode(void){  //构造哈夫曼编码
    HCodeType cd;
    int i,j,c,p;
    
    for(i=1;i<=n;i++){
        cd.start=n;
        c=i;
        p=HuffNode[c].parent;
        while(p!=-1){
            if(HuffNode[p].lchild==c)
                cd.bit[cd.start]=0;
            else
                cd.bit[cd.start]=1;
            cd.start--;
            c=p;
            p=HuffNode[c].parent;
        }
        for(j=cd.start+1;j<=n;j++)
            HuffCode[i].bit[j]=cd.bit[j];
        HuffCode[i].start=cd.start;
    } 
}

void PrintHuffCode(void){  //输出每个叶子结点的哈夫曼编码
    int i,j;
    printf("每个叶子结点的哈夫曼编码为:\n");
    for(i=1;i<=n;i++)
    { 
        for(j=HuffCode[i].start+1;j<=n;j++)
            printf("%d",HuffCode[i].bit[j]);
        printf("\n");
    }
}
int main(void){
    printf("输入叶子节点个数\n"); 
    CreateHuffTree();   //构造哈夫曼树
    PrintHuffTree();    //输出哈夫曼树
    CreateHuffCode();   //构造哈夫曼编码
    PrintHuffCode();    //输出每个叶子结点的哈夫曼编码
    return 0;
}