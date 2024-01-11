#ifndef AVL_TREE_H
#define AVL_TREE_H

#include "binarySearchTree.h"
#include "binaryTreeNode.h"

#include <algorithm>

template <typename Comparable>
class avlTree : public binarySearchTree<Comparable> {
public:
    avlTree() : binarySearchTree<Comparable>() {}
    avlTree(const avlTree & rhs) : binarySearchTree<Comparable>(rhs) {}
    avlTree(avlTree && rhs) : binarySearchTree<Comparable>(std::move(rhs)) {}
    ~avlTree() {}
    
    virtual void insert(const Comparable & x) {
        binarySearchTree<Comparable>::insert(x);
        balance(this->root);
    }
    virtual void insert(Comparable && x) {
        binarySearchTree<Comparable>::insert(std::move(x));
        balance(this->root);
    }

private:

    static const int ALLOWED_IMBALANCE = 1;

private:

    virtual void insert(const Comparable & x, binaryTreeNode<Comparable> * & t) {
        binarySearchTree<Comparable>::insert(x, t);
        balance(t);
    }

    virtual void insert(Comparable && x, binaryTreeNode<Comparable> * & t) {
        binarySearchTree<Comparable>::insert(std::move(x), t);
        balance(t);
    }

    virtual void remove(const Comparable & x, binaryTreeNode<Comparable> * & t) {
        binarySearchTree<Comparable>::remove(x, t);
        balance(t);
    }

    int height(binaryTreeNode<Comparable> *t) const { return t == nullptr ? -1 : t->height; }

    void balance(binaryTreeNode<Comparable> * & t) {
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

    void rotateWithLeftChild(binaryTreeNode<Comparable> * & k2) {
        binaryTreeNode<Comparable> *k1 = k2->left;
        k2->left = k1->right;
        k1->right = k2;
        k2->height = std::max(height(k2->left), height(k2->right)) + 1;
        k1->height = std::max(height(k1->left), k2->height) + 1;
        k2 = k1;
    }

    void rotateWithRightChild(binaryTreeNode<Comparable> * & k2) {
        binaryTreeNode<Comparable> *k1 = k2->right;
        k2->right = k1->left;
        k1->left = k2;
        k2->height = std::max(height(k2->left), height(k2->right)) + 1;
        k1->height = std::max(height(k1->right), k2->height) + 1;
        k2 = k1;
    }

    void doubleWithLeftChild(binaryTreeNode<Comparable> * & k3) {
        rotateWithRightChild(k3->left);
        rotateWithLeftChild(k3);
    }

    void doubleWithRightChild(binaryTreeNode<Comparable> * & k3) {
        rotateWithLeftChild(k3->right);
        rotateWithRightChild(k3);
    }
};

#endif