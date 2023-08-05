#ifndef LISTISTHEAP_H
#define LISTISTHEAP_H

#include <iostream>
#include <queue>
#include <vector>
#include <cmath>
#include "dsexceptions.h"

using namespace std;

template <typename Comparable>
class LeftistHeap {

private:
    struct LeftistNode {
        Comparable element;
        LeftistNode *left;
        LeftistNode *right;
        int npl;
    
        LeftistNode(const Comparable & e, LeftistNode *lt = nullptr, LeftistNode *rt = nullptr, int np = 0)
            : element{e}, left{lt}, right{rt}, npl{np} { }
        LeftistNode(Comparable && e, LeftistNode *lt = nullptr, LeftistNode *rt = nullptr, int np = 0)
            : element{std::move(e)}, left{lt}, right{rt}, npl{np} { }
    };

    LeftistNode *root;

public:
    LeftistHeap( ) : root { nullptr } { }
    LeftistHeap(const LeftistHeap & rhs) : root { nullptr } {
        root = clone(rhs.root);
    }
    LeftistHeap(LeftistHeap && rhs) : root { rhs.root } {
        rhs.root = nullptr;
    }

    ~LeftistHeap( ) { makeEmpty( ); }

    LeftistHeap & operator=(const LeftistHeap & rhs) {
        LeftistHeap copy = rhs;
        std::swap(*this, copy);
        return *this;
    }
    LeftistHeap & operator=(LeftistHeap && rhs) {
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
        root = merge( new LeftistNode { x }, root );
    }
    void insert(Comparable && x) {
        root = merge( new LeftistNode { std::move(x) }, root );
    }

    void deleteMin( ) {
        if (isEmpty( ))
            throw UnderflowException { };
        LeftistNode *oldRoot = root;
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

    void merge(LeftistHeap & rhs) {
        if (this == &rhs)
            return ;
        root = merge(root, rhs.root);
        rhs.root = nullptr;
    }

    void show() {
        vector<Comparable> array;
        array.resize(1);
        change2array(array, root, 0);
        int count = 0;
        int level = 0;
        for (int i = 0; i < array.size(); i++) {
            if (array[i] != 0) {
                cout << array[i] << " ";
                count++;
            } else {
                cout << ". ";
                count++;
            }
            if (count == pow(2, level)) {
                cout << endl;
                count = 0;
                level++;
            }
        }
    }

    void change2array(vector<Comparable> & array, LeftistNode *t, int index) {
        if (t != nullptr) {
            array[index] = t->element;
            if (array.size() < 2 * index + 2)
                array.resize(2 * array.size() + 1);
            change2array(array, t->left, 2 * index + 1);
            change2array(array, t->right, 2 * index + 2);
        }
    }


private:
    LeftistNode * merge(LeftistNode *h1, LeftistNode *h2) {
        if (h1 == nullptr)
            return h2;
        if (h2 == nullptr)
            return h1;
        if (h1->element < h2->element)
            return merge1(h1, h2);
        else
            return merge1(h2, h1);
    }
    LeftistNode * merge1(LeftistNode *h1, LeftistNode *h2) {
        if (h1->left == nullptr)
            h1->left = h2;
        else {
            h1->right = merge(h1->right, h2);
            if (h1->left->npl < h1->right->npl)
                swapChildren(h1);
            h1->npl = h1->right->npl + 1;
        }
        return h1;
    }

    void swapChildren(LeftistNode *t) {
        LeftistNode *tmp = t->left;
        t->left = t->right;
        t->right = tmp;
    }

    void reclaimMemory(LeftistNode *t) {
        if (t != nullptr) {
            reclaimMemory(t->left);
            reclaimMemory(t->right);
            delete t;
        }
    }
    
    LeftistNode * clone(LeftistNode *t) const {
        if (t == nullptr)
            return nullptr;
        else
            return new LeftistNode { t->element, clone(t->left), clone(t->right), t->npl };
    }

};

#endif