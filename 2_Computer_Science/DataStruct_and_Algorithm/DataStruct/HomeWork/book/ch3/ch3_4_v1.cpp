// two sorted list are given, create a new list which is the intersection of the two lists

#include <iostream>

using namespace std;

template <typename Object>
class LinkList {
private:
    struct Node {
        Object data;
        Node *next;
        Node() : next(nullptr) {}
    };
    Node *head, *tail;

public:
    LinkList() : head(new Node), tail(new Node) { head->next = tail; }
    ~LinkList() { clear(); delete head; delete tail; }

    void push_front(const Object &x) {
        Node *newNode = new Node; 
        newNode->data = x; newNode->next = head->next;
        head->next = newNode;  
    }
    void traverse() const { auto p = begin(); while (p != end()) { cout << *p << " "; ++p; } cout << endl; }
    void clear() { 
        while (head->next != tail) {
            Node *tmp = head->next;
            head->next = tmp->next;
            delete tmp;
        }
    }
    
public:
    class const_iterator {
    public:
        const_iterator() : current(nullptr) {}
        const_iterator(Node *p) : current(p) {}
        const Object &operator*() const { return retrieve(); }
        const_iterator &operator++() { current = current->next; return *this; }
        const_iterator operator++(int) { const_iterator old = *this; ++(*this); return old; }
        bool operator==(const const_iterator &rhs) const { return current == rhs.current; }
        bool operator!=(const const_iterator &rhs) const { return !(*this == rhs); }
    protected:
        Object &retrieve() const { return current->data; }
    protected:
        Node *current;
    };
    const_iterator begin() const { return const_iterator(head->next); }
    const_iterator end() const { return const_iterator(tail); }
};


int main() {

    LinkList<int> list1, list2, list3;

    for (int i = 0; i < 10; ++i) {
        list1.push_front(i);
        list2.push_front(i * 2);
    }

    list1.traverse(); // 9 8 7 6 5 4 3 2 1 0
    list2.traverse(); // 18 16 14 12 10 8 6 4 2 0
    auto p1 = list1.begin(), p2 = list2.begin();
    while (p1 != list1.end() && p2 != list2.end()) {
        if (*p1 == *p2) {
            list3.push_front(*p1);
            ++p1; ++p2;
        } else if (*p1 > *p2) {
            ++p1;
        } else {
            ++p2;
        }
    }

    list3.traverse();

    return 0;
}