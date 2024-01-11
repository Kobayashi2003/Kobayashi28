#include <iostream>
#include <stack>
#include <queue>

using namespace std;

struct Node {
    int data;
    Node *lchild;
    Node *rchild; 
};

struct Wrapper {
    Node *node;
    bool visFlg;

    Wrapper(Node *node, bool visFlg) 
        : node(node), visFlg(visFlg) {}
};

struct TestSign {};

class BinaryTree {

private:

    Node *root;

public:

    BinaryTree() : root(nullptr) {}

    explicit BinaryTree(TestSign) {
        queue<Node *> q;
        root = new Node();
        root->data = 1;
        q.push(root);

        for (int i = 2; i <= 15; ++i) {
            Node *node = new Node();
            node->data = i;
            Node *parent = q.front();
            if (!parent->lchild) {
                parent->lchild = node;
            } else {
                parent->rchild = node;
                q.pop();
            }
            q.push(node);
        }
    }

    void postOrder(Node *node, void (*visit)(Node *node)) {
        stack<Wrapper> s;
        Wrapper w(node, false);
        s.push(w);

        while (!s.empty()) {
            Wrapper w = s.top();
            s.pop();
            if (w.visFlg) {
                visit(w.node);
            } else {
                w.visFlg = true;
                s.push(w);
                if (w.node->rchild)
                    s.push(Wrapper(w.node->rchild, false));
                if (w.node->lchild)
                    s.push(Wrapper(w.node->lchild, false));
            }
        } 
    } 

    void printXpar(Node * node, int x, void (*visit)(Node *node)) {
        if (!node)
            return;
        if ((node->lchild && node->lchild->data == x) || (node->rchild && node->rchild->data == x)) {
            if (node == root)
                return;
            visit(node);
        } else {
            if (node->lchild)
                printXpar(node->lchild, x, visit);
            if (node->rchild)
                printXpar(node->rchild, x, visit);
        }
    }

    Node *getRoot() { return root; }

};

int main() {

    TestSign ts;
    BinaryTree bt(ts);

    void (*visit)(Node *node) = [](Node *node) {
        cout << node->data << " ";
    };

    bt.postOrder(bt.getRoot(), visit);
    cout << endl;

    bt.printXpar(bt.getRoot(), 8, visit);
    cout << endl;

    return 0;
}