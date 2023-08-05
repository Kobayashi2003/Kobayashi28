#include "binaryTree.h"
#include "binaryTreeNode.h"

template <typename E>
class linkedBinaryTree : public binaryTree< binaryTreeNode<E> > {
public:
    linkedBinaryTree() { root = nullptr; treeSize = 0; }
    ~linkedBinaryTree() { erase(); }
    bool empty() const { return treeSize == 0; }
    int size() const { return treeSize; }

    void height() const
        { return height(root); }
    void preOrder(void (*theVisit)(binaryTreeNode<E>*)) 
        { visit = theVisit; preOrder(root); }
    void inOrder(void (*theVisit)(binaryTreeNode<E>*)) 
        { visit = theVisit; inOrder(root); }
    void postOrder(void (*theVisit)(binaryTreeNode<E>*)) 
        { visit = theVisit; postOrder(root); }
    void levelOrder(void (*theVisit)(binaryTreeNode<E>*)) 
        { visit = theVisit; levelOrder(root); }
    void erase() {
        postOrder(dispose);
        root = nullptr;
        treeSize = 0;
    }
private:
    binaryTreeNode<E>* root;
    int treeSize;
    static void (*visit) (binaryTreeNode<E>*);
    static int height(binaryTreeNode<E>* t);
    static void preOrder(binaryTreeNode<E>* t);
    static void inOrder(binaryTreeNode<E>* t);
    static void postOrder(binaryTreeNode<E>* t);
    static void levelOrder(binaryTreeNode<E>* t);
    static void dispose(binaryTreeNode<E>* t) { delete t; }
};


template <typename E>
int linkedBinaryTree<E>::height(binaryTreeNode<E>* t) {
    if (t == nullptr) return 0;
    int hl = height(t->leftChild);
    int hr = height(t->rightChild);
    return 1 + (hl > hr ? hl : hr);
}


template <typename E>
void linkedBinaryTree<E>::preOrder(binaryTreeNode<E> *t) {
    if (t != nullptr) {
        linkedBinaryTree<E>::visit(t);
        preOrder(t->leftChild);
        preOrder(t->rightChild);
    }
}


template <typename E>
void linkedBinaryTree<E>::inOrder(binaryTreeNode<E> *t) {
    if (t != nullptr) {
        inOrder(t->leftChild);
        linkedBinaryTree<E>::visit(t);
        inOrder(t->rightChild);
    }
}


template <typename E>
void linkedBinaryTree<E>::postOrder(binaryTreeNode<E> *t) {
    if (t != nullptr) {
        postOrder(t->leftChild);
        postOrder(t->rightChild);
        linkedBinaryTree<E>::visit(t);
    }
}


template <typename E>
void linkedBinaryTree<E>::levelOrder(binaryTreeNode<E> *t) {
    arrayQueue<binaryTreeNode<E>*> q;
    binaryTreeNode<E> *tmp;
    if (t != nullptr) {
        q.push(t);
        while (!q.empty()) {
            tmp = q.front();
            q.pop();
            visit(tmp);
            if (tmp->leftChild != nullptr)
                q.push(tmp->leftChild);
            if (tmp->rightChild != nullptr)
                q.push(tmp->rightChild);
        }
    }
}


