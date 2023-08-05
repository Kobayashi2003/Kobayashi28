// 写本次代码主要是为了练习数据结构

//包括 数据的输入 哈夫曼树的构造 哈夫曼密码的导出 以及哈夫曼解码的实现

//工作报告：截至2022年2月12日 以上内容均已成功实现

//2022/3/2 加入表格导出的功能

//后期将考虑引入ASE加密算法

#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#define MAX ((int)10e5)
#define LEN (sizeof(Haffman_NODE))
#define PER_CAPISITY 10
#define CODESIZE 10
#define STACKSIZE 100
#define DATASIZE 100
#define LEFT 1
#define RIGHT 0

char *EndFlag = "11111111111111111111111111111111";

typedef char DATA_TYPE;
char *FORMAT = "%c";

typedef struct DATA
{
    DATA_TYPE *data;
    int *cont;
    int size;     //表示线性表中的有效数据数
    int capisity; //表示线性表的容量
    int n;        //表示线性表扩增的倍数
} SeqList;

typedef struct Haffman_NODE
{
    DATA_TYPE data;
    int power;
    struct Haffman_NODE *left;  //将权值较小的放于左子树
    struct Haffman_NODE *right; //将权值较大的放于右子树
    struct Haffman_NODE *next;
} Haffman_NODE, FAKE_NODE;

typedef struct
{
    Haffman_NODE *next;
} HEAD, ROOT;

typedef struct Haffman_CODE
{
    DATA_TYPE data;
    int *code;
    int codeSize;
    int capisity;
    int n;
    struct Haffman_CODE *next;
} Haffman_CODE;

typedef struct newTree
{
    DATA_TYPE data;
    struct newTree *left;
    struct newTree *right;
} newTree;

// TODO 一个加密函数还没写
void ASE_Encryption() //加密函数
{
}

/*
//加密对象
DATA_TYPE DATA[]="          *             ,\n                       _/^\\_\n                      <     >\n     *                 /.-.\\         *\n              *        '/&\\'                   *\n                      ,@.*;@,\n                     /_o.I %_\\    *\n        *           (''--:o(_@;\n                   /';--.,__ '')             *\n                  ;@'o % O,*'''&\n            *    (''--)_@ ;o %'()\\      *\n                 /';--._'''--._O'@;\n                /&*,()~o';-.,_ '\"\"')\n     *          /',@ ;+& () o*';-';\n               ('\"\"--.,_0o*';-' &()\n               /-.,_    ''''--....-'')  *\n          *    /@%;o':;'--,.__   __.'\n              ;*,&(); @ % &^;~'\"'o;@();         *\n              /()Emily & ().o@Robin%O\n              '\"=\"==\"\"==,,,.,=\"==\"===\"'\n         __.----.(\\-''#####---...___...-----._\n         ''         \\)_'\"\"\"\"\"'\n                        .--' ')\n                      o(  )_-\n                       '\"\"\"' '";
//解密对象
char *HaffmanCode="0000000000000000000000000010110000000000000000000000000000000101111110000000000000000000000000010011000000000000000000000000000000110111101000000000000000000000000001000110000000000000000000000000000011111110010000000000000000000000000010010100000000000000000000000000000111111100000000000000000000000000000101101000000000000000000000000000001001110000000000000000000000000001110110000000000000000000000000000010111011000000000000000000000000001010100000000000000000000000000000010111010000000000000000000000000001000100000000000000000000000000000010111001000000000000000000000000001011110000000000000000000000000000011011000100000000000000000000000001000000000000000000000000000000000001101100000000000000000000000000000011110100000000000000000000000000000110101111000000000000000000000000011011110000000000000000000000000000011010111000000000000000000000000000001010000000000000000000000000000001011011000000000000000000000000000100111000000000000000000000000000001001010000000000000000000000000010111110000000000000000000000000000010110011000000000000000000000000010011110000000000000000000000000000100010010111000000000000000000000000011111100000000000000000000000000000100110010110100000000000000000000000001101001000000000000000000000000000010011001011000000000000000000000000000101110000000000000000000000000000000111100101000000000000000000000000000101000000000000000000000000000000001101001000000000000000000000000000010111000000000000000000000000000000101100010000000000000000000000000010100100000000000000000000000000000110100001000000000000000000000000011011010000000000000000000000000000101010000011110000000000000000000000000110110000000000000000000000000000001010100000111000000000000000000000000000110000000000000000000000000000000010101000001101000000000000000000000000010001010000000000000000000000000000101010000011000000000000000000000000000110001000000000000000000000000000001010100000101100000000000000000000000001101110000000000000000000000000000010101000001010000000000000000000000000011110010000000000000000000000000000101010000010010000000000000000000000000101001000000000000000000000000000001010100000100000000000000000000000000001011110000000000000000000000000000010011000000110000000000000000000000000011101000000000000000000000000000001001100000010000000000000000000000000010010010000000000000000000000000000101010000000110000000000000000000000000010101100000000000000000000000000001010100000001000000000000000000000000000111100000000000000000000000000000010101000000001000000000000000000000000001111100000000000000000000000000000101010000000000000000000000000000000000010000000000000000000000000000000000001011111111111111111111111111111111000000000011010000000000000011111101100000000000000000000000010011110001100000011100101010011101100000000000000000000000100000000100000100000000010110000001101000000000000000000110001100011110100011001010000000000110101011000000000000000110100000000010101100011111011001010101000000000000000000001101010110000000000000000000000011111110000100011101011011110000111111011000000000000000000000011000110011101110100011000000011011110001001110010100000110101011000000000110100000000000010010010101010111011101000000101011101001001001111000011011101100000000000000000000110001101011011111011101000111111100111001101010101010000100000000000001101010110000000000000000000110111100001010101110011110000100101111111111010101010101010111101101100000000000001101000001001001010101011101110100001100111100000110111011100111100010101001001000011001010000000110101011000000000000000000110001101011011111011101000110011101010101010111011101000110011100101111010110000110111011000000000000000001100011111011101011111100100100001100101101101110101011011111010001111111001101010110011100110101000011011000000110100000000000110001101011111110000011011100000001011110101001001000010101110110101010110111110101011011101100000000000000001001001010110011100111101110100011111110011100000110110111011010101011011111010100111101100100100001101100000000000000001100011110100011111110011000010101010101010101110111010001100011000110001111010101010100001001101010110000000000011010000011000111000011110001101110111010101000000101101110101110111011111100011001110011000100111001110001101010110000000000000001101111010111111111011001001000011101101100000111100001111011000000111101110010110110101100110101011101101111000010010010000111011000000000110101011000000000000000110001100100100001100000110010000011111001011001000001110100000100101111010100100100001100011011101100001000001000101110100000101110010110010000010101111000100101111011000000000000000101011001101111110011011111011111100111001101111101111111111111111111100011111110111111001101111101111110011011111011111011111100110101011000000000010011100111000111101110111011101000110010010010101110101010101111001111100111110011111001111100111101110111010001100011000110011100111001110001100011000111101110111011101110100011001110110000000000101010100000000001001010100001100111010110011100111001110011100110101011000000000000000000000000010001111011101010010101000011011000000000000000000000001011101001000010000110011111010110000000000000000000000001010110011100111001101001010";
*/

DATA_TYPE DATA[] = "Please input the data you want to change into Haffman code here.";

//PLease input the Haffman code you want to translate here:
char *HaffmanCode = "00000000000000000000000001110100000000000000000000000000000000111110000000000000000000000000110100000000000000000000000000000000100110100000000000000000000000001100100000000000000000000000000000001011100100000000000000000000000001100011000000000000000000000000000001011100000000000000000000000000001100101000000000000000000000000000000111010000000000000000000000000110000100000000000000000000000000000011100000000000000000000000000011001110000000000000000000000000000011001111100000000000000000000000001001000000000000000000000000000000001100111100000000000000000000000000111100100000000000000000000000000000110011101000000000000000000000000011101110000000000000000000000000000011001110000000000000000000000000001101111000000000000000000000000000001000110000000000000000000000000011010010000000000000000000000000000010101011000000000000000000000000011101010000000000000000000000000000010101010000000000000000000000000011100110000000000000000000000000000011001001100000000000000000000000001110000000000000000000000000000000001100100100000000000000000000000000101000000000000000000000000000000000110010001000000000000000000000000011011000000000000000000000000000000011001000000000000000000000000000001100110000000000000000000000000000001010011100000000000000000000000000101110000000000000000000000000000001100011010000000000000000000000000110110100000000000000000000000000000111001100100000000000000000000000001110010000000000000000000000000000001110011000000000000000000000000000011011100000000000000000000000000000010000100000000000000000000000000010000000000000000000000000000000000011000111111111111111111111111111111110100010100001011000100111010000101100100100100101011100011111011010001100110011110000001110101100101000001110010000101110001110110000110001101100001001111110100001011001011101100000111101000011100111001100110000100001100001101100110100011011010011000101001101";

bool SHOW_TABLE = true;
bool InputFile = false;
bool TEST = false;
bool AUTO_INPUT = true;

int main()
{
    int screen(void);
    void createHaffmanTree(DATA_TYPE *, int *, int);
    void deCode(int);
    void deCode_AUTO(char *);
    // TODO 妥协 受不了了 理想的输入应该是可以在终端中接受包括换行符在内的所有字符 并且输入最终以EOF作为收尾 但试验后发现一般的scanf或者getchar结合循环的输入方式会出现bug 因此相关的输入结构升级放由今后解决

    SeqList Table; //用于记录共有多少种的字符
    Table.data = (DATA_TYPE *)malloc(PER_CAPISITY * sizeof(DATA_TYPE));
    Table.cont = (int *)malloc(PER_CAPISITY * sizeof(int));
    Table.size = 0;
    Table.capisity = PER_CAPISITY;
    Table.n = 1;

    int num = 0;

    switch (screen())
    {
    case 1:
        assert(sizeof(DATA) / sizeof(DATA_TYPE) - 1 > 1);
        for (int i; i < (sizeof(DATA) / sizeof(DATA_TYPE)); i++)
        {
            for (int j = 0; j <= Table.size; j++)
            {
                if (j < Table.size && DATA[i] == Table.data[j])
                {
                    Table.cont[j]++;
                    break;
                }
                else if (j == Table.size)
                {
                    if (Table.size == Table.capisity)
                    {
                        Table.n++;
                        Table.capisity = PER_CAPISITY * Table.n;
                        Table.data = (DATA_TYPE *)realloc(Table.data, Table.capisity * sizeof(DATA_TYPE));
                        Table.cont = (int *)realloc(Table.cont, Table.capisity * sizeof(int));
                    }
                    Table.data[Table.size] = DATA[i];
                    Table.cont[Table.size] = 1;
                    Table.size++;
                    break;
                }
            }
        }
        createHaffmanTree(Table.data, Table.cont, Table.size - 1);
        break;

    case 2:
        if (AUTO_INPUT)
        {
            deCode_AUTO(HaffmanCode);
        }
        else
        {
            printf("Input the number of the types of code: ");
            scanf("%d", &num);
            deCode(num);
        }
        break;
    }
    return 0;
}

int screen(void)
{
    int num;
    printf("What do you want to do?\n[1]ENCODE\n[2]DECODE\n");
    printf("INPUT:[ ]\b\b");
    scanf("%d", &num);
    return num;
}

void createHaffmanTree(DATA_TYPE *data, int *table, int cont) //这里将构建一个真正的树结构与一个链表结构 并且两个结构的结点将会共用
{
    bool countNode(HEAD *);
    void deleteNode(HEAD *, Haffman_NODE *);
    void insertNode(HEAD *, FAKE_NODE *);
    void createCodeTable(ROOT *, int);
    HEAD *head = (HEAD *)malloc(sizeof(HEAD));
    head->next = NULL;
    Haffman_NODE *tmp = NULL;
    for (int i = 0; i < cont; i++)
    {
        Haffman_NODE *newnode = (Haffman_NODE *)malloc(LEN);
        newnode->data = data[i];
        newnode->power = table[i];
        newnode->left = NULL;
        newnode->right = NULL;
        newnode->next = NULL;
        if (i == 0)
        {
            head->next = newnode;
        }
        else
        {
            tmp->next = newnode;
        }
        tmp = newnode;
    }

    //这里还需要设置一个循环 直到整个链表只剩下一个元素为止 (考虑是否需要为链表添加一个无意义的头结点 同时可能需要为哈夫曼树增添一个树结点)
    //循环应从此处开始 并且为了确认终止条件（当链表中只剩下一个结点的时候） 需要再写一个链表结点计数函数
    ROOT root;
    root.next = NULL;
    while (countNode(head))
    {

        Haffman_NODE *find1 = NULL, *find2 = NULL;
        int num1 = MAX, num2 = MAX;
        tmp = head->next;
        do
        {
            if (tmp->power < num1)
            {
                num2 = num1;
                find2 = find1;
                num1 = tmp->power;
                find1 = tmp;
            }
            else if (tmp->power < num2)
            {
                num2 = tmp->power;
                find2 = tmp;
            }
            tmp = tmp->next;
        } while (tmp != NULL);

        //到这里为止基本雏形已经有了 剩下只需要将权值最小的两个结点从链表中删去 并将伪结点加入到链表中即可
        FAKE_NODE *fNode = (FAKE_NODE *)malloc(LEN);
        fNode->left = find1;
        fNode->right = find2;
        fNode->power = num1 + num2;
        root.next = fNode;

        deleteNode(head, find1);
        deleteNode(head, find2);
        insertNode(head, fNode);
    }
    //到这里哈夫曼树已经形成 此时root中的next所指的即为最后一个伪结点 即树根 接下来就是导出哈夫曼编码
    createCodeTable(&root, cont);
}

void deleteNode(HEAD *head, Haffman_NODE *node) //不能将一个结点真正意义上的删除 只能将其排除出链表
{
    if (head->next == node)
    {
        head->next = node->next;
        node->next = NULL;
    }
    else
    {
        Haffman_NODE *tmp = head->next;
        while (tmp->next != node)
        {
            tmp = tmp->next;
        }
        tmp->next = node->next;
        node->next = NULL;
    }
}

void insertNode(HEAD *head, FAKE_NODE *fNode) //这里用头插法
{
    Haffman_NODE *tmp = head->next;
    head->next = fNode;
    fNode->next = tmp;
}

bool countNode(HEAD *head)
{
    int cont = 0;
    Haffman_NODE *tmp = head->next;
    while (tmp != NULL)
    {
        cont++;
        tmp = tmp->next;
    }
    return (cont == 1) ? 0 : 1;
}

void createCodeTable(ROOT *root, int cont) //哈夫曼编码在后面需要用于对data数据的转化 因此哈夫曼编码需要保存 哈夫曼编码一般由0 1组成 可储存于数组中 为了保证储存的准确性 最好采用线性表的储存方式
{
    void createBlankList(Haffman_CODE *, int);
    void push(Haffman_NODE **, Haffman_NODE *, int *, int, int *);
    void pop(int *);
    void isfull(int);
    void displayElem(Haffman_CODE *, Haffman_NODE *, int *, int);
    Haffman_NODE *getTop(Haffman_NODE **, int *);
    int getMemory(int *, int *);
    void createArray(Haffman_CODE **, Haffman_CODE *, int);
    void quicksort(Haffman_CODE **, int, int);
    void change(DATA_TYPE *, Haffman_CODE, int);
    //遍历哈夫曼树(因为需要保存哈夫曼编码 因此最好采用非递归的遍历方式) 一直遍历到叶结点之后 保存从根结点到该叶结点的路径
    //规定 进入左子树记为 0  进入右子树 1(哈夫曼树中的某一结点若存在子结点 则它必同时存在左右子树）
    //如果使用c99中的变长数组或者使用realloc函数进行处理的话问题将会简化许多 但这里为了程序易于移植 采用建立动态链表的方式储存哈夫曼编码
    Haffman_CODE CODE;
    CODE.code = NULL;
    CODE.codeSize = 0;
    CODE.capisity = 0;
    CODE.n = 0;
    CODE.next = NULL;
    createBlankList(&CODE, cont);
    //接下来就是找到所有的叶结点 并将遍历哈夫曼时的路径转换为哈夫曼编码进行储存
    Haffman_CODE *tmp = CODE.next;

    int save[10]; //用于临时保存编码
    int len = 0;  //记录到当前结点编码的长度

    //结合栈结构遍历哈夫曼树
    Haffman_NODE *stack[STACKSIZE] = {NULL};
    int memory[STACKSIZE] = {0};

    Haffman_NODE *p;
    int top = -1;
    push(stack, root->next, memory, len, &top);
    while (top != -1)
    {
        p = getTop(stack, &top); //取栈顶元素
        if (p != root->next)
        {
            len = getMemory(memory, &top); //动态规划查找
            save[len - 1] = RIGHT;
        }
        pop(&top);

        while (p->left != NULL)
        {
            //若当前结点非叶结点，则让当前结点的右子结点进栈
            len++;
            push(stack, p->right, memory, len, &top);
            isfull(top);
            p = p->left;
            save[len - 1] = LEFT;
        }

        displayElem(tmp, p, save, len);
        tmp = tmp->next;
    }
    printf(EndFlag);

    if (SHOW_TABLE)
    {
        Haffman_CODE **Array = (Haffman_CODE **)malloc(cont * sizeof(Haffman_CODE *));
        printf("\n\n");
        createArray(Array, &CODE, cont);
        quicksort(Array, 0, cont - 1);
        printf("The number of codes:%d\n", cont);
        tmp = CODE.next;

        if (InputFile)
        {
            FILE *file=fopen("D:/DATA.txt","w+");
            while (tmp != NULL)
            {
                fprintf(file,"| ");
                if (tmp->data == '\n')
                {
                    fprintf(file,"\b\\n");
                }
                else
                {
                    fprintf(file,FORMAT, tmp->data);
                }
                fprintf(file," |");
                fprintf(file,"  ");
                for (int i = 0; i < tmp->codeSize; i++)
                {
                    fprintf(file,"%d", tmp->code[i]);
                }
                fprintf(file,"\n");
                tmp = tmp->next;
            }
        }

        else
        {
            while(tmp!=NULL)
            {
                printf("| ");
                if (tmp->data == '\n')
                {
                    printf("\b\\n");
                }
                else
                {
                    printf(FORMAT, tmp->data);
                }
                printf(" |");
                printf("  ");
                for (int i = 0; i < tmp->codeSize; i++)
                {
                    printf("%d", tmp->code[i]);
                }
                printf("\n");
                tmp = tmp->next;
            }
        }
        printf("\n");
    }
    change(DATA, CODE, sizeof(DATA) / sizeof(DATA_TYPE));
}

void createBlankList(Haffman_CODE *CODE, int cont) //生成一个空链表用于储存哈夫曼编码
{
    Haffman_CODE *tmp = CODE;
    for (int i = 0; i < cont; i++)
    {
        Haffman_CODE *newNode = (Haffman_CODE *)malloc(sizeof(Haffman_CODE));
        newNode->code = (int *)malloc(CODESIZE * sizeof(int));
        newNode->codeSize = 0;
        newNode->capisity = CODESIZE;
        newNode->n = 1;
        newNode->next = NULL;
        tmp->next = newNode;
        tmp = newNode;
    }
}

void push(Haffman_NODE **stack, Haffman_NODE *elem, int *memory, int len, int *top) //前序遍历使用的进栈函数
{
    stack[++(*top)] = elem;
    memory[(*top)] = len;
}

void pop(int *top) //弹栈函数
{
    if (*top == -1)
    {
        return;
    }
    (*top)--;
}

void isfull(int top)
{
    assert((top <= STACKSIZE)); //本来应该是用动态顺序表来进行内存扩张的 之后再说叭
}

void displayElem(Haffman_CODE *CODE, Haffman_NODE *elem, int *save, int codeLen) //模拟操作结点元素的函数
{
    void ASCII_Encode(int);

    if (codeLen > CODE->capisity)
    {
        CODE->capisity *= codeLen;
        CODE->code = (int *)realloc(CODE->code, sizeof(int) * CODE->capisity);
    }
    CODE->data = elem->data;
    CODE->codeSize = codeLen;
    for (int i = 0; i < codeLen; i++)
    {
        CODE->code[i] = save[i];
    }
    if (AUTO_INPUT == true)
    {
        if (TEST)
            printf("TEST POINT 1:\n");
        ASCII_Encode((int)(CODE->data));
        if (TEST)
            printf("\n");
        if (TEST)
            printf("TEST POINT 2:\n");
        ASCII_Encode(CODE->codeSize);
        if (TEST)
            printf("\n");
        if (TEST)
            printf("TEST POINT 3:\n");
        for (int i = 0; i < codeLen; i++)
        {
            printf("%d", CODE->code[i]);
        }
        if (TEST)
            printf("\n");
    }
}

Haffman_NODE *getTop(Haffman_NODE **stack, int *top)
{
    return stack[*top];
}

int getMemory(int *memory, int *top)
{
    return memory[*top];
}

void createArray(Haffman_CODE **Array, Haffman_CODE *CODE, int cont)
{
    Haffman_CODE *p = CODE->next;
    for (int i = 0; i < cont; i++)
    {
        Array[i] = p;
        p = p->next;
    }
}

void ASCII_Encode(int num) //将两个信息转换为二进制之后输出 1、字符对应的ASCII码 2、字符对应的哈夫曼编码的长度
{
    //并且 必须保证最后输出的二进制码为 4 字节 即 32 位
    int code[32] = {0}, ord, cont = 0;
    if (TEST)
        printf("the number:%d\n", num);
    while (num)
    {
        ord = 0;
        code[ord]++;
        num--;
        while (code[ord] - 2 == 0)
        {
            code[ord] = 0;
            code[++ord]++;
            cont = (ord > cont ? ord : cont);
        }
    }
    for (int i = 31; i >= 0; i--)
    {
        printf("%d", code[i]);
    }
}

void quicksort(Haffman_CODE **Array, int low, int high) //用于整理编码
{
    int spilt(Haffman_CODE **, int, int);
    int middle;
    if (low >= high)
        return;
    middle = spilt(Array, low, high);
    quicksort(Array, low, middle - 1);
    quicksort(Array, middle + 1, high);
}

int spilt(Haffman_CODE **Array, int low, int high)
{
    int compare(int *, int *, int);
    DATA_TYPE tmp_data = Array[low]->data;
    int *tmp_code = Array[low]->code;
    int tmp_codeSize = Array[low]->codeSize;
    int tmp_capisity = Array[low]->capisity;
    int tmp_n = Array[low]->n;
    for (;;)
    {
        while (low < high && tmp_codeSize <= Array[high]->codeSize)
        {
            if (tmp_codeSize == Array[high]->codeSize)
                if (compare(tmp_code, Array[high]->code, tmp_codeSize) == 0)
                    break;
            high--;
        }
        if (low >= high)
            break;

        Array[low]->data = Array[high]->data;
        Array[low]->code = Array[high]->code;
        Array[low]->codeSize = Array[high]->codeSize;
        Array[low]->capisity = Array[high]->capisity;
        Array[low]->n = Array[high]->n;
        low++;

        while (low < high && Array[low]->codeSize <= tmp_codeSize)
        {
            if (Array[low]->codeSize == tmp_codeSize)
                if (compare(Array[low]->code, tmp_code, tmp_codeSize) == 0)
                    break;
            low++;
        }
        if (low >= high)
            break;
        Array[high]->data = Array[low]->data;
        Array[high]->code = Array[low]->code;
        Array[high]->codeSize = Array[low]->codeSize;
        Array[high]->capisity = Array[low]->capisity;
        Array[high]->n = Array[low]->n;
        high--;
    }
    Array[high]->data = tmp_data;
    Array[high]->code = tmp_code;
    Array[high]->codeSize = tmp_codeSize;
    Array[high]->capisity = tmp_capisity;
    Array[high]->n = tmp_n;
    return high;
}

int compare(int *x, int *y, int len)
{
    //规定x大于y返回 0 x小于y返回 1 x等于y返回 2
    for (int i = 0; i < len; i++)
    {
        if (x[i] > y[i])
            return 0;
        else if (x[i] < y[i])
            return 1;
    }
    return 2;
}

void change(DATA_TYPE *data, Haffman_CODE CODE, int dataLen)
{
    if (SHOW_TABLE)
        printf("The Haffman Code is:\n");
    for (int i = 0; i < dataLen - 1; i++)
    {
        Haffman_CODE *tmp = CODE.next;
        while (tmp != NULL && tmp->data != data[i])
        {
            tmp = tmp->next;
        }
        assert(tmp != NULL);
        for (int j = 0; j < tmp->codeSize; j++)
        {
            printf("%d", tmp->code[j]);
        }
        //        putchar(' ');
    }
}

void deCode(int num) //对一串哈夫曼转换后的密码进行解码
{
    void createBlankList(Haffman_CODE *, int);
    void rebuildHaffmanTree(Haffman_CODE, newTree *);
    Haffman_CODE CODE;
    CODE.code = NULL;
    CODE.codeSize = 0;
    CODE.capisity = 0;
    CODE.n = 0;
    CODE.next = NULL;
    createBlankList(&CODE, num);
    Haffman_CODE *tmp = CODE.next;
    char c;
    while (tmp != NULL)
    {
        c = '\0';
        printf("Input the data:");
        fflush(stdin);
        scanf(FORMAT, &tmp->data);
        fflush(stdin);
        printf("Input the Haffman code:");
        for (; (c = getchar()) != '\n'; tmp->codeSize++)
        {
            if (tmp->codeSize == tmp->capisity)
            {
                tmp->n++;
                tmp->capisity = tmp->n * CODESIZE;
                tmp->code = (int *)realloc(tmp->code, sizeof(int) * tmp->capisity);
            }
            assert(c - '0' == 0 || c - '0' == 1);
            tmp->code[tmp->codeSize] = c - '0';
        }
        tmp = tmp->next;
    }
    fflush(stdin);
    //建立一颗新树
    newTree Head;
    Head.left = NULL;
    Head.right = NULL;
    rebuildHaffmanTree(CODE, &Head);
    //接下来就是翻译哈夫曼编码
    int *data = (int *)malloc(sizeof(int) * DATASIZE), n = 1;
    printf("Input the code you want to translate:");
    int len;
    newTree *p = &Head;
    for (len = 0; (c = getchar()) != '\n'; len++)
    {
        if (len == (n * DATASIZE))
        {
            data = (int *)realloc(data, (++n) * DATASIZE * sizeof(int));
        }
        assert(c - '0' == 0 || c - '0' == 1);
        data[len] = c - '0';
    }
    for (int i = 0; i < len; i++)
    {
        switch (data[i])
        {
        case LEFT:
            p = p->left;
            assert(p != NULL);
            break;
        case RIGHT:
            p = p->right;
            assert(p != NULL);
            break;
        }
        if (p->left == NULL && p->right == NULL)
        {
            printf(FORMAT, p->data);
            p = &Head;
        }
    }
}

void deCode_AUTO(char *HaffmanCode)
{
    bool isEnd(char *);
    int ASCII_Decode(char *);
    void rebuildHaffmanTree(Haffman_CODE, newTree *);

    if (HaffmanCode[0] == '\0')
    {
        printf("Input the Haffamn code you want to decode:\n");
        fflush(stdin);
        char c;
        int len = 0;
        while ((c = getchar()) != '\n')
        {
            if (len == 0)
            {
                HaffmanCode = (char *)malloc(sizeof(char));
                HaffmanCode[len] = c;
                len++;
            }
            else
            {
                HaffmanCode = (char *)realloc(HaffmanCode, ++len * sizeof(char));
                HaffmanCode[len - 1] = c;
            }
        }
        HaffmanCode[len] = '\0';
    }
    char *p = &HaffmanCode[0];
    Haffman_CODE headNode;
    Haffman_CODE *tmp = &headNode;
    while (isEnd(p))
    {
        Haffman_CODE *newnode = (Haffman_CODE *)malloc(sizeof(Haffman_CODE));
        newnode->next = NULL;
        newnode->data = (DATA_TYPE)ASCII_Decode(p);
        p += 32;
        newnode->codeSize = ASCII_Decode(p);
        p += 32;
        newnode->code = (int *)malloc(newnode->codeSize * sizeof(int));
        for (int i = 0; i < newnode->codeSize; i++)
        {
            newnode->code[i] = *p - '0';
            p++;
        }
        tmp->next = newnode;
        tmp = newnode;
    }
    p += 32;

    printf("the plain text:\n");
    newTree root;
    root.left = NULL;
    root.right = NULL;
    rebuildHaffmanTree(headNode, &root);
    newTree *temp = &root;
    while (*p != '\0')
    {
        switch (*p - '0')
        {
        case LEFT:
            temp = temp->left;
            assert(temp != NULL);
            break;
        case RIGHT:
            temp = temp->right;
            assert(temp != NULL);
            break;
        default:
            printf("WRONG CODE!");
            exit(0);
        }
        if (temp->left == NULL && temp->right == NULL)
        {
            printf(FORMAT, temp->data);
            temp = &root;
        }
        p++;
    }
}

void rebuildHaffmanTree(Haffman_CODE CODE, newTree *head) //再构造一颗简易的哈夫曼树
{
    Haffman_CODE *tmp = CODE.next;
    newTree *p = NULL;
    while (tmp != NULL)
    {
        p = head;
        for (int i = 0; i < tmp->codeSize; i++)
        {
            switch (tmp->code[i])
            {
            case LEFT:
                if (p->left == NULL)
                {
                    p->left = (newTree *)malloc(sizeof(newTree));
                    p = p->left;
                    p->left = NULL;
                    p->right = NULL;
                }
                else
                {
                    p = p->left;
                }
                break;
            case RIGHT:
                if (p->right == NULL)
                {
                    p->right = (newTree *)malloc(sizeof(newTree));
                    p = p->right;
                    p->left = NULL;
                    p->right = NULL;
                }
                else
                {
                    p = p->right;
                }
                break;
            default:
                exit(0);
            }
            if (i == tmp->codeSize - 1)
            {
                p->data = tmp->data;
            }
        }
        tmp = tmp->next;
    }
}

bool isEnd(char *p)
{
    char tmp[33] = {[32] = '\0'};
    for (int i = 0; i < 32; i++)
    {
        tmp[i] = p[i];
    }
    //    printf("END JUDGE:%d\n",strcmp(tmp,EndFlag));
    if (strcmp(tmp, EndFlag) == 0)
        return false;
    return true;
}

int ASCII_Decode(char *p)
{
    int POW(int, int);
    int num = 0;
    for (int i = 31, j = 0; i >= 0; i--, j++)
    {
        if (*(p + i) - '0' == 1)
        {
            num += POW(2, j);
        }
    }
    return num;
}

int POW(int x, int y)
{
    if (y == 0)
        return 1;
    else if (y % 2 == 0)
    {
        int tmp = POW(x, y / 2);
        return tmp * tmp;
    }
    return x * POW(x, y - 1);
}