#include <queue>
#include <stack>
#include <iostream>
using namespace std;

/**********************************************************************
*********************************
* Helpers
**********************************************************************
*********************************/
template <typename Type>
struct Node {
    Type data;
    Node* left;
    Node* right;
    Node() :left(nullptr), right(nullptr) {}
    Node(Type item, Node* L = nullptr, Node* R = nullptr) :data(item), left(L), right(R) {}
};

template <class Type>
struct StNode
{
    Node<Type>* node;
    int TimesPop;
    StNode(Node<Type>* N = nullptr) : node(N), TimesPop(0) {}
};

template <class elemType>
class linkStack : public stack<elemType>
{
private:
    struct node {
        elemType data;
        node* next;
        node(const elemType& x, node* N = nullptr) { data = x; next = N; }
        node() :next(nullptr) {}
        ~node() {}
    };
    node* elem;
public:
    linkStack() { elem = nullptr; }
    ~linkStack() {
        node* tmp;
        while (elem != nullptr) {
            tmp = elem;
            elem = elem->next;
            delete tmp;
        }
    }

    bool isEmpty() { return elem == nullptr; }

    void push(const elemType& x) {
        node* tmp = new node(x, elem);
        elem = tmp;
    }

    elemType pop() {
        node* tmp = elem;
        elemType x = tmp->data;
        elem = elem->next;
        delete tmp;
        return x;
    }

    elemType top() { return elem->data; }

    void makeEmpty() {
        node* tmp;
        while (elem != nullptr) {
            tmp = elem;
            elem = elem->next;
            delete tmp;
        }
        elem = nullptr;
    }
};

/**********************************************************************
*********************************
* 二叉树
**********************************************************************
*********************************/
template <class Type>
class BinaryTree {
public:
    Node<Type>* root;
    struct stNode {
        Node<Type>* node;
        int TimesPop;
        stNode(Node<Type>* N = nullptr) :node(N), TimesPop(0) {}
    };

public:
    BinaryTree() :root(nullptr) {}

    BinaryTree(const Type& value) {
        root = new Node<Type>(value);
    }
    ~BinaryTree() {
        clear();
    }

    void clear() {
        if (root != nullptr)
        clear(root);
        root = nullptr;
    }

    void createTree(Type flag) {
        queue<Node<Type>*> que;
        Node<Type>* tmp;
        Type x, ldata, rdata;
        cin >> x;
        root = new Node<Type>(x);
        que.push(root);
        while (!que.empty())
        {
            tmp = que.front();
            que.pop();
            cin >> ldata >> rdata;
            if (ldata != flag)
                que.push(tmp->left = new Node<Type>(ldata));
            if (rdata != flag)
                que.push(tmp->right = new Node<Type>(rdata));
        }
    }

private:
    void clear(Node<Type>* t) {
        if (t->left != nullptr)
            clear(t->left);
        if (t->right != nullptr)
            clear(t->right);
        delete t;
        return;
    }
};

/**********************************************************************
*********************************
* 迭代器基类
**********************************************************************
*********************************/
template <class Type>
class TreeIterator {
public:
    TreeIterator(const BinaryTree<Type>& BT) : T(BT), current(nullptr) {}
    virtual ~TreeIterator() {}
    // 第一个被访问的结点地址送 current
    virtual void First() = 0;
    // 下一个被访问的结点地址送 current
    virtual void operator++() = 0;
    // 判当前结点为空吗， 为空返回 True
    bool operator+() const { return current != nullptr; }
    // 返回当前结点指针 current 所指向的结点的数据值。
    Type& operator()() const { return current->data; }

public:
    const BinaryTree<Type>& T;
    // BinaryTree<Type>::Node* current;
    Node<Type>* current;
    // 指向当前结点的指针。
};

/**********************************************************************
*********************************
* 前序遍历迭代器
**********************************************************************
*********************************/
template <class Type>
class Preorder : public TreeIterator<Type>
{
public:
    Preorder(const BinaryTree<Type>& R) : TreeIterator<Type>(R) { s.push(this->T.root); }
    ~Preorder() {}

    void First() {
        s.makeEmpty();
        if (this->T.root) s.push(this->T.root);
        operator++();
    }
    void operator++() {
        if (s.isEmpty()) {
            this->current = nullptr; return;
        }
        // 得到当前结点的地址， 并进行出栈操作。
        this->current = s.top();
        s.pop();

        // push right child first, then left child
        if (this->current->right) s.push(this->current->right);
        if (this->current->left) s.push(this->current->left);
    }
protected:
    linkStack<Node<Type> *> s;
};

/**********************************************************************
*********************************
* 后序遍历迭代器
**********************************************************************
*********************************/
template <class Type>
class Postorder : public TreeIterator<Type>
{
    public:
    Postorder(const BinaryTree < Type >& R) : TreeIterator<Type>(R) {
        s.push(StNode<Type>(this->T.root));
    }
    ~Postorder() { }

    // 后序遍历时的第一个结点的地址。
    void First() {
        // 得到第一个访问的结点地址

        s.makeEmpty();
        if (this->T.root) s.push(StNode<Type>(this->T.root));
        operator++();

    }
    // 后序遍历时的下一个结点的地址。
    void operator++() {
        if (s.isEmpty())
        { // 当栈空且 current 也为空时， 遍历结束。
            this->current = nullptr;
            return;
        } // 置当前指针为空，结束。
        StNode<Type> Cnode;
        for (; ; )
        {
            Cnode = s.top();
            this->s.pop();
            if (Cnode.TimesPop == 0)
            { // 第一次访问该结点
                Cnode.TimesPop++;
                this->s.push(Cnode);
                if(Cnode.node->left) s.push(StNode<Type>(Cnode.node->left));
            }
            else if (Cnode.TimesPop == 1)
            { // 第二次访问该结点
                Cnode.TimesPop++;
                this->s.push(Cnode);
                if(Cnode.node->right) s.push(StNode<Type>(Cnode.node->right));
            }
            else
            { // 第三次访问该结点
                this->current = Cnode.node;
                return;
            }
        }
    }
protected:
    linkStack<StNode<Type>> s;
};

/**********************************************************************
*********************************
* 中序遍历迭代器
**********************************************************************
*********************************/
template <class Type> class Inorder: public Postorder < Type >
{
public:
    Inorder(const BinaryTree < Type >& R): Postorder<Type>(R) { }
    void operator++(); // 中序时的下一个结点的地址。
};

template <class Type>
void Inorder<Type>::operator++()
{
    if (this->s.isEmpty())
    { // 当栈空且 current 也为空时， 遍历结束。
        this->current = nullptr; return;
    } // 置当前指针为空， 结束。
    StNode<Type> Cnode;
    for (; ; )
    {
        Cnode = this->s.top();
        this->s.pop();
        if (Cnode.TimesPop == 0) {
            Cnode.TimesPop++;
            this->s.push(Cnode);
            if (Cnode.node->left) this->s.push(StNode<Type>(Cnode.node->left));
        }
        else if (Cnode.TimesPop == 1) {
            this->current = Cnode.node;
            if (Cnode.node->right) this->s.push(StNode<Type>(Cnode.node->right));
            return;
        }
        else if (Cnode.TimesPop == 2) {
            this->current = Cnode.node;
            return;
        }
    }

}

/*
**********************************************************************
*********************************
* 主函数
**********************************************************************
*********************************/
int main()
{
    BinaryTree<int> tree;
    tree.createTree(-1);

    Preorder<int> pre(tree);
    for (pre.First(); +pre; ++pre)
        cout << pre() << ' ';
    cout << endl;

    Inorder<int> in(tree);
    for (in.First(); +in; ++in)
        cout << in() << ' ';
    cout << endl;

    Postorder<int> post(tree);
    for (post.First(); +post; ++post)
        cout << post() << ' ';
    return 0;
}