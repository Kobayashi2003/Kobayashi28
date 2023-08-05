#ifndef _BINOMIAL_QUEUE_H
#define _BINOMIAL_QUEUE_H

#include <vector>

using namespace std;

template <typename Comparable> 
class BiQueue {
private:
    struct BiqueNode {
        Comparable element;
        BiqueNode *lchild = nullptr;
        BiqueNode *sibling = nullptr;
        BiqueNode( const Comparable & e ) : element { e } {}
        BiqueNode( Comparable && e ) : element { move(e) } {}
    };

    vector< BiqueNode* > biQue;

    BiqueNode * combine(BiqueNode *p, BiqueNode *q) {
        if (p->element > q->element)
            return combine(q, p);
        else {
            q->sibling = p->lchild;
            p->lchild = q;
        }
        return p; 
    }

public:
    BiqueNode * insert(Comparable v) { 
        BiqueNode * t = new BiqueNode(v);
        BiqueNode * c = t;
        if (biQue.empty()) {
            biQue.push_back(c);
            return t;
        }
        for (size_t i = 0; i <= biQue.size(); ++i) {
            if (i == biQue.size() - 1)
                biQue.push_back(nullptr);
            if (biQue[i] == nullptr) {
                biQue[i] = c;
                break; 
            } else {
                c = combine(c, biQue[i]);
                biQue[i] = nullptr;
            }
        }
        return t;
    }
};

#endif