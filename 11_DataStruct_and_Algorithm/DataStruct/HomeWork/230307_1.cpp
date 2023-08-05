#include <iostream>
using namespace std;
template <typename T>

struct Node
{
    Node *next;
    T value;
};

template <typename T>
class List
{
public:
    Node<T> *head;
    List() : head(nullptr){};
    ~List()
    {
        Node<T> *p;
        while (head != nullptr)
        {
            p = head;
            head = head->next;
            delete p;
        }
    }

    void insert(T value)
    /*
    函数名：insert
    输入值：泛型 value
    功  能：向队列中插入一个节点，值为value，使得表内元素实现有序排列（从小到大）
     */
    {
        Node<T> *p = head;              //获得头节点指针
        Node<T> *node = new Node<T>;    //创建新的节点
        node->value = value;
        node->next = nullptr;
        if (p == nullptr)               //如果头节点为空，直接将新节点作为头节点
        {
            head = node;
            return;
        }
        if (p->value > value)           //如果头节点的值大于新节点的值，将新节点插入到头节点之前
        {
            node->next = p;
            head = node;
            return;
        }
        while (p->next != nullptr)      //遍历链表，找到第一个大于新节点的值的节点
        {
            if (p->next->value > value)
                break;
            p = p->next;
        }
        node->next = p->next;           //将新节点插入到该节点之前
        p->next = node;
    }

    void printAll()
    /*
    函数名：printAll
    输入值：无
    功  能：遍历并输出线性表
     */
    {
        Node<T> *p = head;
        if (p == nullptr)
        {
            cout << endl;
            return;
        }
        cout << p->value;
        p = p->next;
        while (p != nullptr)
        {
            cout << " " << p->value;
            p = p->next;
        }
        cout << endl;
    }

    void merge(List<T> *l2)
    /*
    函数名：merge
    输入值：队列地址
    功  能：合并两个线性表
     */
    {
        Node<T> *p1 = head;
        Node<T> *p2 = l2->head;
        Node<T> *p = nullptr;
        Node<T> *q = nullptr;
        if (p1 == nullptr)
        {
            head = p2;
            return;
        }
        if (p2 == nullptr)
            return;
        if (p1->value > p2->value)
        {
            head = p2;
            p2 = p2->next;
        }
        else
        {
            p1 = p1->next;
        }
        p = head;
        while (p1 != nullptr && p2 != nullptr)
        {
            if (p1->value > p2->value)
            {
                p->next = p2;
                p2 = p2->next;
            }
            else
            {
                p->next = p1;
                p1 = p1->next;
            }
            p = p->next;
        }
        if (p1 == nullptr)
            p->next = p2;
        else
            p->next = p1;
    }
};
template <typename T>
void test()
{
    int N1, N2;
    T value;
    List<T> l1, l2;
    cin >> N1;
    for (; N1 > 0; N1--)
    {
        cin >> value;
        l1.insert(value);
    }
    l1.printAll();
    cin >> N2;
    for (; N2 > 0; N2--)
    {
        cin >> value;
        l2.insert(value);
    }
    l2.printAll();
    l1.merge(&l2);
    l1.printAll();
}
int main()
{
    string dtype;
    cin >> dtype;
    if (dtype == "int")
        test<int>();
    else
        test<float>();
    return 0;
}