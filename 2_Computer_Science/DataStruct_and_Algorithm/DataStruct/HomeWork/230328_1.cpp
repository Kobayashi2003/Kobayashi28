#include <queue>
#include <stack>
#include <iostream>

using namespace std;

template <class Type>
class BinaryTree {
private:

    struct Node {
        Type data;
        Node* left;
        Node* right;

        Node() :left(nullptr), right(nullptr) {}
        Node(Type item, Node* L = nullptr, Node* R = nullptr) :data(item), left(L), right(R) {}

        ~Node() {}
    };
    Node* root;

public:
    BinaryTree() :root(nullptr) {}
    BinaryTree(const Type& value) {
        root = new Node(value);
    }

    Type getRoot() const { return root->data; }
    Type getLeft() const { return root->left->data; }
    Type getRight() const { return root->right->data; }

    void makeTree(const Type& x, BinaryTree& lt, BinaryTree& rt) {
        root = new Node(x, lt.root, rt.root);
        lt.root = nullptr;
        rt.root = nullptr;
    }

    int size() const { return size(root); }
    int height() const { return height(root); }

    void preOrder() const {
        if (root != nullptr) {
            preOrder(root);
        }
        cout << endl;
    }

    void midOrder() const {
        if (root != nullptr) {
            midOrder(root);
        }
        cout << endl;
    }

    void postOrder() const {
        if (root != nullptr) {
            postOrder(root);
        }
        //cout << endl;
    }
    // 此处输入等于 flag 表示该位置没有节点的情况
    void createTree(float flag) {
        queue<Node*> que;
        Node* tmp;
        Type x, ldata, rdata;
        cin >> x;
        if (x == flag) {
            root = nullptr;
            return;
        }
        root = new Node(x);
        que.push(root);
        while (!que.empty())
        {
            tmp = que.front();
            que.pop();
            cin >> ldata >> rdata;
            if (ldata != flag)
            que.push(tmp->left = new Node(ldata));
            if (rdata != flag)
            que.push(tmp->right = new Node(rdata));
        }
    }

private:
    //递归求树高
    int height(Node* t) const {
        if (t == nullptr)
            return 0;
        int l_height = height(t->left);
        int r_height = height(t->right);
        return l_height > r_height ? l_height + 1 : r_height + 1;
    }

    void clear(Node* t) {
        if (t->left != nullptr)
            clear(t->left);
        if (t->right != nullptr)
            clear(t->right);
        delete t;
        //t = nullptr;
        return;
    }

    //递归求树大小
    int size(Node* t) const {
        if (t == nullptr)
            return 0;
        return size(t->left) + size(t->right) + 1;
    }
    //递归实现
    void preOrder(Node *t) const{

        if (t == nullptr)
            return;
        cout << t->data << ' ';
        preOrder(t->left);
        preOrder(t->right);

    }
    //递归实现
    void midOrder(Node *t) const{

        if (t == nullptr)
            return;

        midOrder(t->left);
        cout << t->data << ' ';
        midOrder(t->right);

    }
    //递归实现
    void postOrder(Node *t) const{

        if (t == nullptr)
            return;

        postOrder(t->left);
        postOrder(t->right);
        cout << t->data << ' ';

    }
};


int main() {
    int x;
    BinaryTree<int> tree, tree1, tree2;
    //第一颗树的构建，-1 作为没有子节点的标志
    tree.createTree(-1);
    cout << tree.height() << ' ' << tree.size() << endl;

    //第二颗树的构建
    tree1.createTree(-1);
    cout << tree1.height() << ' ' << tree1.size() << endl;

    //合并两棵树，x 为根节点的值
    cin >> x;
    tree2.makeTree(x, tree, tree1);
    cout << tree2.height() << ' ' << tree2.size() << endl;
    tree2.preOrder();
    tree2.midOrder();
    tree2.postOrder();

    return 0;
}
