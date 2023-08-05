#ifndef _BinomialQueue_H
#define _BinomialQueue_H

#include <vector>

using namespace std;

template <typename Comparable>
struct BiQueNode {
    Comparable item;
    vector<BiQueNode *> pointers;
    BiQueNode<Comparable> (Comparable e) : item(e) { }
};

template <typename Comparable>
class BinomialQue {
private:
    vector<BiQueNode<Comparable>> biQue;
};

template <typename Comparable>
BiQueNode<Comparable> * combine(BiQueNode<Comparable> * p, BiQueNode<Comparable> * q) {
    if (p->item > q->item) {
        return combine(q, p);
    }
    else {
        p->pointers.push_back(q);
        return p;
    }
}

template <typename Comparable>
BiQueNode<Comparable> * insert(Comparable v) {
    BiQueNode<Comparable> * t = new BiQueNode<Comparable>(v);
    BiQueNode<Comparable> * c = t;
    for (int i = 0; i <= biQue.size(); i++) {
        if (c == nullptr) break;
        if (i == biQue.size() - 1)
            biQue.push_back(nullptr);
        if (biQue[i] == nullptr) {
            biQue[i] = c;
            break;
        }
        else {
            c = combine(c, biQue[i]);
            biQue[i] = nullptr;
        }
    }
    return t;
}

#endif 