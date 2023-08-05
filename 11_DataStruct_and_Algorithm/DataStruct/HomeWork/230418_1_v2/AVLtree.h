#ifndef _AVL_TREE_H_
#define _AVL_TREE_H_

#include <iostream>

template <typename Comparable>
class AVLtree {
private:

    class Node {
    public:
        explicit Node(const Comparable & _elem, Node *_lchild = nullptr, Node * _rchild = nullptr, Node * _parent = nullptr, int _balance = 0) 
            : elem{ _elem }, lchild{ _lchild }, rchild{ _rchild }, parent{ _parent }, height{ 0 }, balance { 0 } {} 
        explicit Node(Comparable && _elem, Node *_lchild = nullptr, Node * _rchild = nullptr, Node * _parent = nullptr, int _balance = 0)
            : elem{ std::move(_elem) }, lchild{ _lchild }, rchild{ _rchild }, parent{ _parent }, height { 0 }, balance { 0 } {} 
    public:
        Comparable elem;
        Node *lchild;
        Node *rchild;
        Node *parent;
        int height;
        int balance;
    };
    Node *root;
    static const int ALLOWED_INBALANCE = 1;
    static void (*visit)(const Comparable & elem);

private:

    int height(Node * node) const { return node == nullptr ? -1 : node->height; }
    void rotateL(Node *k1) {
        Node *k2 = k1->rchild;
        k1->rchild = k2->lchild;
        if (k1->rchild != nullptr)
            k1->rchild->parent = k1;
        k2->lchild = k1;
        k2->parent = k1->parent;
        k1->parent = k2;
        
        if (k2->parent == nullptr)
            root = k2;
        else if (k2->parent->lchild == k1)
            k2->parent->lchild = k2;
        else
            k2->parent->rchild = k2;

        int l_height = height(k1->lchild);
        int r_height = height(k1->rchild);
        k1->height = std::max(l_height, r_height) + 1;
        k1->balance = l_height - r_height;

        l_height = height(k2->lchild);
        r_height = height(k2->rchild);
        k2->height = std::max(l_height, r_height) + 1;
        k2->balance = l_height - r_height;

        return;
    }
    void rotateR(Node *k1) {
        Node *k2 = k1->lchild;
        k1->lchild = k2->rchild;
        if (k1->lchild != nullptr)
            k1->lchild->parent = k1;
        k2->rchild = k1;
        k2->parent = k1->parent;
        k1->parent = k2;

        if (k2->parent == nullptr)
            root = k2;
        else if (k2->parent->lchild == k1)
            k2->parent->lchild = k2;
        else
            k2->parent->rchild = k2;

        int l_height = height(k1->lchild);
        int r_height = height(k1->rchild);
        k1->height = std::max(l_height, r_height) + 1;
        k1->balance = l_height - r_height;

        l_height = height(k2->lchild);
        r_height = height(k2->rchild);
        k2->height = std::max(l_height, r_height) + 1;
        k2->balance = l_height - r_height;
    
        return;
    }
    void updateblance(Node *node) {
        if (node == nullptr) return ;
        node->balance = height(node->lchild) - height(node->rchild); 
    }
    void rebalance(Node *node) {
        if (node == nullptr) return ;

        int balance = node->balance;
        if (balance < -1) {
            if (node->rchild->balance > 0)
                rotateR(node->rchild);
            rotateL(node);
        }
        else if (balance > 1) {
            if (node->lchild->balance < 0)
                rotateL(node->lchild);
            rotateR(node);
        }
        else {
            node->height = std::max(height(node->lchild), height(node->rchild)) + 1;
        }
    }

    void preOrder(Node *node) const {
        if (node == nullptr) return ;
        visit(node->elem);
        preOrder(node->lchild);
        preOrder(node->rchild);
    }
    void inOrder(Node *node) const {
        if (node == nullptr) return ;
        inOrder(node->lchild);
        visit(node->elem);
        inOrder(node->rchild);
    }

public:

    AVLtree(Node * _root = nullptr) : root{_root} {}

    void insert(const Comparable & _elem) {
        if (root == nullptr) {
            root = new Node(_elem);
            return ;
        }
        Node *p = root;
        while (true) {
            if (_elem == p->elem)
                return ;
            else if (_elem < p->elem) {
                if (p->lchild == nullptr) {
                    p->lchild = new Node(_elem, nullptr, nullptr, p);
                    break;
                }
                else {
                    p = p->lchild;
                }
            }
            else {
                if (p->rchild == nullptr) {
                    p->rchild = new Node(_elem, nullptr, nullptr, p);
                    break;
                }
                else {
                    p = p->rchild;
                }
            }
        }
        while (p != nullptr) {
            updateblance(p);
            rebalance(p);
            p = p->parent;
        }
    }
    void insert(Comparable && _elem) {
        if (root == nullptr) {
            root = new Node(std::move(_elem));
            return ;
        }

        Node *p = root;
        while (true) {
            if (_elem == p->elem)
                return ;
            else if (_elem < p->elem) {
                if (p->lchild == nullptr) {
                    p->lchild = new Node(std::move(_elem), nullptr, nullptr, p);
                    break;
                }
                else {
                    p = p->lchild;
                }
            }
            else {
                if (p->rchild == nullptr) {
                    p->rchild = new Node(std::move(_elem), nullptr, nullptr, p);
                    break;
                }
                else {
                    p = p->rchild;
                }
            }
        }
        while (p != nullptr) {
            updateblance(p);
            rebalance(p);
            p = p->parent;
        }
    }

    void preOrder(void (*func)(const Comparable & elem)) const { visit = func; preOrder(root); }
    void inOrder(void (*func)(const Comparable & elem)) const { visit = func; inOrder(root); }

    void preOrder() const { visit = [](const Comparable & elem) { std::cout << elem << " "; }; preOrder(root); }
    void inOrder() const { visit = [](const Comparable & elem) { std::cout << elem << " "; }; inOrder(root); }
};

template <typename Comparable>
void (*AVLtree<Comparable>::visit)(const Comparable & elem) = nullptr;

#endif