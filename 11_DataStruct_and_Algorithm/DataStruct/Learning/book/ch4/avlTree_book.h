#ifndef _AVLTREE_BOOK_H
#define _AVLTREE_BOOK_H

#include <iostream>

template <typename Comparable>
class AvlTree {
private:
    struct AvlNode {
        Comparable element;
        AvlNode *left;
        AvlNode *right;
        int height;

        AvlNode(const Comparable & ele, AvlNode *lt, AvlNode *rt, int h = 0)
            : element{ ele }, left{ lt }, right{ rt }, height{ h } { }
        AvlNode(Comparable && ele, AvlNode *lt, AvlNode *rt, int h = 0)
            : element{ std::move(ele) }, left{ lt }, right{ rt }, height{ h } { }
    };

    AvlNode *root = nullptr;

    static const int ALLOWED_IMBALANCE = 1;

public:

    int height(AvlNode *t) const { return t == nullptr ? -1 : t->height; }

    void insert(const Comparable & x) { insert(x, root); }
    void insert(Comparable && x) { insert(std::move(x), root); }

    void remove(const Comparable & x) { remove(x, root); }

    bool isEmpty() const { return root == nullptr; }

    void preOrder() const { preOrder(root); }
    void inOrder() const { inOrder(root); }

private:

    void preOrder(AvlNode *t) const {
        if (t == nullptr)
            return;
        std::cout << t->element << " ";
        preOrder(t->left);
        preOrder(t->right);
    }


    void inOrder(AvlNode *t) const {
        if (t == nullptr)
            return;
        inOrder(t->left);
        std::cout << t->element << " ";
        inOrder(t->right);
    }

    
    void insert(const Comparable & x, AvlNode * & t) {
        if (t == nullptr)
            t = new AvlNode{ x, nullptr, nullptr };
        else if (x < t->element)
            insert(x, t->left);
        else if (t->element < x)
            insert(x, t->right);
        else
            ; // Duplicate; do nothing
        
        balance(t);
    }

    void balance(AvlNode * & t) {
        if (t == nullptr)
            return;
        if (height(t->left) - height(t->right) > ALLOWED_IMBALANCE) {
            if (height(t->left->left) >= height(t->left->right))
                rotateWithLeftChild(t);
            else
                doubleWithLeftChild(t);
        }
        
        else if (height(t->right) - height(t->left) > ALLOWED_IMBALANCE) {
            if (height(t->right->right) >= height(t->right->left))
                rotateWithRightChild(t);
            else
                doubleWithRightChild(t);
        }
            
        t->height = std::max(height(t->left), height(t->right)) + 1;
    }

    void rotateWithLeftChild(AvlNode * & k2) {
        AvlNode *k1 = k2->left;
        k2->left = k1->right;
        k1->right = k2;
        k2->height = std::max(height(k2->left), height(k2->right)) + 1;
        k1->height = std::max(height(k1->left), k2->height) + 1;
        k2 = k1;
    }

    void rotateWithRightChild(AvlNode * & k2) {
        AvlNode *k1 = k2->right;
        k2->right = k1->left;
        k1->left = k2;
        k2->height = std::max(height(k2->left), height(k2->right)) + 1;
        k1->height = std::max(height(k1->right), k2->height) + 1;
        k2 = k1;
    }

    void doubleWithLeftChild(AvlNode * & k3) {
        rotateWithRightChild(k3->left);
        rotateWithLeftChild(k3);
    }

    void doubleWithRightChild(AvlNode * & k3) {
        rotateWithLeftChild(k3->right);
        rotateWithRightChild(k3);
    }

    void remove(const Comparable & x, AvlNode * & t) {
        if (t == nullptr)
            return ; // Item not found; do nothing
        if (x < t->element)
            remove(x, t->left);
        else if (t->element < x)
            remove(x, t->right);
        else if (t->left != nullptr && t->right != nullptr) { // Two children
            t->element = findMin(t->right)->element;
            remove(t->element, t->right);
        }
        else {
            AvlNode *oldNode = t;
            t = (t->left != nullptr) ? t->left : t->right;
            delete oldNode;
        }
        balance(t);
    }
};

#endif