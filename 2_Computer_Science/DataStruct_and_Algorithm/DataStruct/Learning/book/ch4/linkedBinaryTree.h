#ifndef LINKED_BINARY_TREE_H
#define LINKED_BINARY_TREE_H
#include <iostream>
#include <utility>
#include "binaryTree.h"
#include "binaryTreeNode.h"

template <typename Object>
class linkedBinaryTree : public binaryTree<binaryTreeNode<Object> > {
public:

    typedef binaryTreeNode<Object> Node;
    Node *root;

public:
    explicit linkedBinaryTree() : root(nullptr) {}
    explicit linkedBinaryTree(const Object value) : root(new Node(value)) {}
    explicit linkedBinaryTree(Node *p) : root(p) {}

    virtual ~linkedBinaryTree() { delTree(); }

    Object getRoot() const { return root->data; }
    Object getLeft() const { return root->left->data; }
    Object getRight() const { return root->right->data; }

    void makeTree(const Object &x, linkedBinaryTree<Object> &lt, linkedBinaryTree<Object> &rt);

    void delLeft() {
        linkedBinaryTree tmp = root->left;
        root->left = nullptr;
        tmp.delTree();
    } 
    void delRight() {
        linkedBinaryTree tmp = root->right;
        root->right = nullptr;
        tmp.delTree();
    }
    void delTree() { if (root != nullptr) delTree(root); }

    bool empty() const { return root == nullptr;}
    int size() const { return size(root); }
    int height() const { return height(root); }

    void preOrder(void (*theVisit)(Node *)) { visit = theVisit; preOrder(root); }
    void inOrder(void (*theVisit)(Node *)) { visit = theVisit; inOrder(root); }
    void postOrder(void (*theVisit)(Node *)) { visit = theVisit; postOrder(root); }

    void preOrder() { preOrder(visit); }
    void inOrder() { inOrder(visit); }
    void postOrder() { postOrder(visit); }


protected:

    static void (*visit)(Node *);

    void delTree(Node *t) {
        if (t->left != nullptr) delTree(t->left);
        if (t->right != nullptr) delTree(t->right);
        delete t;
    }

    int size(Node *t) const {
        if (t == nullptr) return 0;
        return 1 + size(t->left) + size(t->right);
    }

    int height(Node *t) const {
        if (t == nullptr) return 0;
        int hl = height(t->left), hr = height(t->right);
        return 1 + (hl > hr ? hl : hr);
    }
    
    void preOrder(Node *t) {
        if (t == nullptr) return;
        visit(t);
        preOrder(t->left);
        preOrder(t->right);
    }

    void inOrder(Node *t) {
        if (t == nullptr) return;
        inOrder(t->left);
        visit(t);
        inOrder(t->right);
    }

    void postOrder(Node *t) {
        if (t == nullptr) return;
        postOrder(t->left);
        postOrder(t->right);
        visit(t);
    }

};

template <typename Object>
void (*linkedBinaryTree<Object>::visit)(linkedBinaryTree<Object>::Node *) = [](linkedBinaryTree<Object>::Node *t) { std::cout << t->data << " "; };


template <typename Object>
void linkedBinaryTree<Object>::makeTree(const Object &x, linkedBinaryTree<Object> &lt, linkedBinaryTree<Object> &rt) {
    root = new Node(x, lt.root, rt.root);
    lt.root = rt.root = nullptr;
}

#endif