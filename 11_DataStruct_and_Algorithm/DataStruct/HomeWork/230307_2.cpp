#include <iostream>
using namespace std;
/*
设计循环链表解决约瑟夫问题：
给定一组输入数据 a0, a1, ...,aN（int 型、float 型或 char 型），
选取 x(x>=1)作为计数上限，从 a0 开始按顺序报数，将第 x 个元素出列。
x 之后的第一个元素继续从 1 开始报数，报到 x 的元素再出列，重复该过程 y 次（y<=数组长度）。
*/

template <typename T>
struct Node
{ // 定义节点
    Node *next;
    T value;
};

template <typename T>
class List
{ // 定义单向循环链表
public:
    Node<T> *record; // 定义当前操作指针(null)
    int length;
    List() : record(nullptr), length(0){}; // 初始化链表
    ~List() { delete record; }

    void insert(T value)
    /*
    函数名：insert
    输入值：泛型 value
    功  能：向循环链表中插入一个节点，值为value
     */
    {
        Node<T> *node = new Node<T>; // 新加入节点 node
        node->value = value;         // 新节点 node 赋值
        node->next = nullptr;        // 新节点的 next 节点
        length = length + 1;         // 链表长度增加
        if (record == nullptr)
        { // 若 record 为空，则链表为空，将新节点作为头节点
            record = node;
            record->next = record;
            return;
        }
        Node<T> *p = record;
        while (p->next != record)
        { // 通过顺序循环，将当前操作指针移动到链表尾部
            p = p->next;
        }
        p->next = node; // 将新节点插入到链表尾部
        node->next = record;
    }

    T pop(int position)
    /*
    函数名：pop
    输入值：整型 position
    功  能：将position位置的节点进行出队，返回值为该节点
     */
    {
        for (int i = 1; i < position-1; i++) // 通过顺序循环，将当前操作指针移动到被删除节点的前驱
            record = record->next;

        Node<T> *p = record->next;    // 被删除节点
        record->next = p->next;       // 删除节点
        T temp = p->value;
        delete p;                     // 智能指针删除节点
        p = nullptr;                       // 智能指针删除节点
        length = length - 1;               // 元素出栈后，链表长度减一
        record = record->next;             // 当前操作指针指向下一个节点
        return temp;
    }

    void printAll()
    /*
    函数名：printAll
    输入值：无
    功  能：遍历并输出队列
     */
    {
        Node<T> *p = record;
        if (p == nullptr)
        { // 若 record 为空，则链表为空，输出为空
            cout << endl;
            return;
        }
        cout << p->value; // 否则输出头指针的值
        while (p->next != record)
        { // 通过顺序循环，输出链表中的所有元素
            cout << " " << p->next->value;
            p = p->next;
        }
        cout << endl;
    }
};

template <typename T>
void test()
{
    int length, position, circle;
    T value;
    List<T> mylist;
    cin >> length;
    for (; length > 0; length--)
    {
        cin >> value;
        mylist.insert(value);
    }
    mylist.printAll();
    cin >> position;
    cin >> circle;
    for (int i = 0; i < circle; i++)
    {
        cout << mylist.pop(position) << endl;
    }
    mylist.printAll();
}

int main()
{
    string dtype;
    cin >> dtype;
    if (dtype == "int")
        test<int>();
    else if (dtype == "float")
        test<float>();
    else
        test<char>();
    return 0;
}