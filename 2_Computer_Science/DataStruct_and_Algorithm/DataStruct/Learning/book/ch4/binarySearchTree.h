#ifndef BINARY_SEARCH_TREE_H
#define BINARY_SEARCH_TREE_H
#include "linkedBinaryTree.h"

using namespace std;


template <typename Comparable>
class binarySearchTree : public linkedBinaryTree<Comparable> {

public:
    explicit binarySearchTree() : linkedBinaryTree<Comparable>() {}
    explicit binarySearchTree(const Comparable &value) : linkedBinaryTree<Comparable>(value) {}
    explicit binarySearchTree(binarySearchTree<Comparable> *p) : linkedBinaryTree<Comparable>(p) {}

    virtual ~binarySearchTree() { }

    bool find(const Comparable &x) const { return find(x, this->root); }
    virtual void insert(const Comparable &x) { insert(x, this->root); }
    virtual void remove(const Comparable &x) { remove(x, this->root); }

protected:

    bool find(const Comparable &x, binaryTreeNode<Comparable> *t) const;
    virtual void insert(const Comparable &x, binaryTreeNode<Comparable> *&t);
    virtual void remove(const Comparable &x, binaryTreeNode<Comparable> *&t);
    void removeMax(binaryTreeNode<Comparable> *&t, Comparable &x);
    void removeMin(binaryTreeNode<Comparable> *&t, Comparable &x);
    void removeNode(binaryTreeNode<Comparable> *&t);
    binaryTreeNode<Comparable> *findMin(binaryTreeNode<Comparable> *t) const;
    binaryTreeNode<Comparable> *findMax(binaryTreeNode<Comparable> *t) const;
};

template <typename Comparable>
bool binarySearchTree<Comparable>::find(const Comparable &x, binaryTreeNode<Comparable> *t) const {
    if (t == nullptr) return false;
    else if (x < t->data) return find(x, t->left);
    else if (x > t->data) return find(x, t->right);
    else return true;
}

template <typename Comparable>
void binarySearchTree<Comparable>::insert(const Comparable &x, binaryTreeNode<Comparable> *&t) {
    if (t == nullptr) t = new binaryTreeNode<Comparable>(x, nullptr, nullptr);
    else if (x < t->data) insert(x, t->left);
    else if (x > t->data) insert(x, t->right);
    else ;
}

template <typename Comparable>
void binarySearchTree<Comparable>::remove(const Comparable &x, binaryTreeNode<Comparable> *&t) {
    if (t == nullptr) return;
    if (x < t->data) remove(x, t->left);
    else if (x > t->data) remove(x, t->right);
    else removeNode(t);
}

template <typename Comparable>
void binarySearchTree<Comparable>::removeMax(binaryTreeNode<Comparable> *&t, Comparable &x) {
    if (t->right == nullptr) {
        x = t->data;
        binaryTreeNode<Comparable> *oldNode = t;
        t = t->left;
        delete oldNode;
    } else {
        removeMax(t->right, x);
    }
}

template <typename Comparable>
void binarySearchTree<Comparable>::removeMin(binaryTreeNode<Comparable> *&t, Comparable &x) {
    if (t->left == nullptr) {
        x = t->data;
        binaryTreeNode<Comparable> *oldNode = t;
        t = t->right;
        delete oldNode;
    } else {
        removeMin(t->left, x);
    }
}

template <typename Comparable>
void binarySearchTree<Comparable>::removeNode(binaryTreeNode<Comparable> *&t) {
    binaryTreeNode<Comparable> *oldNode = t;
    if (t->left == nullptr) t = t->right;
    else if (t->right == nullptr) t = t->left;
    else removeMin(t->right, t->data);
    delete oldNode;
}

template <typename Comparable>
binaryTreeNode<Comparable> *binarySearchTree<Comparable>::findMin(binaryTreeNode<Comparable> *t) const {
    if (t == nullptr) return nullptr;
    if (t->left == nullptr) return t;
    return findMin(t->left);
}

template <typename Comparable>
binaryTreeNode<Comparable> *binarySearchTree<Comparable>::findMax(binaryTreeNode<Comparable> *t) const {
    if (t == nullptr) return nullptr;
    if (t->right == nullptr) return t;
    return findMax(t->right);
}

#endif