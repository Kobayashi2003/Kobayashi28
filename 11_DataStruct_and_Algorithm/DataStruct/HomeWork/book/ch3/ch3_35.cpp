#include <iostream>
#include <utility>

using namespace std;

template <typename Object>
class circularQueue {
private:
    struct node {
        Object data;
        node *next;
        node() : next(nullptr) {}
        node(const Object &&d, node *n = nullptr) : data(std::move(d)), next(n) {}
    };

public:
    circularQueue() : theSize(0), tail(nullptr) {}
    ~circularQueue() { clear(); }

    bool isEmpty() { return theSize == 0; }
    void clear() { while (!isEmpty()) dequeue(); }

    void enqueue(const Object &&x) {
        if (isEmpty()) {
            tail = new node {std::move(x)};
            tail->next = tail;
        } else {
            tail->next = new node {std::move(x), tail->next};
            tail = tail->next;
        }                     
        ++theSize;                                                                                                           
    }

    void dequeue() {
        if (isEmpty()) return;
        node *old = tail->next;
        if (old == tail) tail = nullptr;
        else tail->next = old->next;
        delete old;
        --theSize;
    }

private:
    int theSize;
    node *tail;
};

int main() {
    circularQueue<int> cq;
    return 0;
}