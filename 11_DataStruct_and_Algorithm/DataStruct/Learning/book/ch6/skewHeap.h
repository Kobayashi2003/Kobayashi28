#ifndef SKEWHEAP_H
#define SKEWHEAP_H

#include <iostream>
#include "dsexceptions.h"

template <typename Comparable>
class SkewHeap {
public:
    SkewHeap( ) : root { nullptr } { }
    SkewHeap(const SkewHeap & rhs) : root { nullptr } {
        root = clone(rhs.root);
    }
    SkewHeap(SkewHeap && rhs) : root { rhs.root } {
        rhs.root = nullptr;
    }

    ~SkewHeap( ) { makeEmpty( ); }

    SkewHeap & operator=(const SkewHeap & rhs) {
        SkewHeap copy = rhs;
        std::swap(*this, copy);
        return *this;
    }
    SkewHeap & operator=(SkewHeap && rhs) {
        std::swap(root, rhs.root);
        return *this;
    }

    bool isEmpty( ) const { return root == nullptr; }

    const Comparable & findMin( ) const {
        if (isEmpty( ))
            throw UnderflowException { };
        return root->element;
    }

    void insert(const Comparable & x) {
        root = merge( new SkewNode { x }, root );
    }
    void insert(Comparable && x) {
        root = merge( new SkewNode { std::move(x) }, root );
    }

    void deleteMin( ) {
        if (isEmpty( ))
            throw UnderflowException { };
        SkewNode *oldRoot = root;
        root = merge(root->left, root->right);
        delete oldRoot;
    }
    void deleteMin(Comparable & minItem) {
        minItem = findMin( );
        deleteMin( );
    }

    void makeEmpty( ) {
        reclaimMemory(root);
        root = nullptr;
    }

    void merge(SkewHeap & rhs) {
        if (this == &rhs)
            return;
        root = merge(root, rhs.root);
        rhs.root = nullptr;
    }

private:
    struct SkewNode {
        Comparable element;
        SkewNode *left;
        SkewNode *right;

        SkewNode(const Comparable & e, SkewNode *lt = nullptr, SkewNode *rt = nullptr)
            : element { e }, left { lt }, right { rt } { }
        SkewNode(Comparable && e, SkewNode *lt = nullptr, SkewNode *rt = nullptr)
            : element { std::move(e) }, left { lt }, right { rt } { }
    };

    SkewNode *root;

    SkewNode *merge(SkewNode *h1, SkewNode *h2) {
        if (h1 == nullptr)
            return h2;
        if (h2 == nullptr)
            return h1;
        if (h1->element < h2->element)
            return merge1(h1, h2);
        else
            return merge1(h2, h1);
    }

    SkewNode *merge1(SkewNode *h1, SkewNode *h2) {
        if (h1->left == nullptr)
            h1->left = h2;
        else {
            h1->right = merge(h1->right, h2);
            std::swap(h1->left, h1->right);
        }
        return h1;
    }

    void reclaimMemory(SkewNode *t) {
        if (t != nullptr) {
            std::cout << "delete " << t->element << std::endl;
            reclaimMemory(t->left);
            reclaimMemory(t->right);
            delete t;
        }
    }

    SkewNode *clone(SkewNode *t) const {
        if (t == nullptr)
            return nullptr;
        else
            return new SkewNode { t->element, clone(t->left), clone(t->right) };
    }

};


#endif