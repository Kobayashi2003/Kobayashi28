#include <iostream>

using namespace std;

struct Node {
    int data;
    Node * left, * right;
};


class BSTree {

private:

    Node * root;

    void preOrder(Node * cur) const {
        if (cur == nullptr) return;
        cout << cur->data << " ";
        preOrder(cur->left);
        preOrder(cur->right);
    }

    void midOrder(Node * cur) const {
        if (cur == nullptr) return;
        midOrder(cur->left);
        cout << cur->data << " ";
        midOrder(cur->right);
    }

    void postOrder(Node * cur) const {
        if (cur == nullptr) return;
        postOrder(cur->left);
        postOrder(cur->right);
        cout << cur->data << " ";
    }

public:

    BSTree() : root(nullptr) {}

    void insert(int data) {
        Node * newNode = new Node;
        newNode->data = data;
        newNode->left = newNode->right = nullptr;

        if (root == nullptr) {
            root = newNode;
            return;
        }

        Node * cur = root;

        while (true) {
            if (data < cur->data) {
                if (cur->left == nullptr) {
                    cur->left = newNode;
                    return;
                }
                cur = cur->left;
            } else {
                if (cur->right == nullptr) {
                    cur->right = newNode;
                    return;
                }
                cur = cur->right;
            }
        }
    }

    void preOrder() const {
        preOrder(root);
        cout << endl;
    }
    
    void midOrder() const {
        midOrder(root);
        cout << endl;
    }

    void postOrder() const {
        postOrder(root);
        cout << endl;
    }
};


int main() {

    int n = 1;
    while (n) {
        BSTree tree;
        cin >> n;
        for (int i = 0; i < n; ++i) {
            int data;
            cin >> data;
            tree.insert(data);
        }
        tree.midOrder();
        tree.preOrder();
    }

    return 0;
}