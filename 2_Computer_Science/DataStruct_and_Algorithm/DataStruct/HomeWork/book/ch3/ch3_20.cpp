// lazy deletion
#include <iostream>

using namespace std;

template <typename Object>
class LazyList {
private:
    struct Node {
        Object data;
        Node *next;
        bool deleted_flag;
        Node(Object d, Node *n = nullptr, bool d_flg = false) : data(d), next(n), deleted_flag(d_flg) {}
        Node() : next(nullptr), deleted_flag(false) {}
    };

public:
    LazyList() : head(new Node), theSize(0), deletedNum(0) {}
    ~LazyList() { clear(); delete head; }

    void clear() {
        if (isEmpty()) return;
        Node *p = head->next;
        while (p != nullptr) {
            Node *tmp = p;
            p = p->next;
            delete tmp;
        }
        head->next = nullptr;
        theSize = 0;
    }

    void deleteNode(Node *pre, Node *deleteNode) {
        pre->next = deleteNode->next;
        delete deleteNode;
        --theSize;
    }
    
    void lazyDelete(Object x) {
        Node *p = head->next;
        while (p != nullptr && p->data != x) {
            p = p->next;
        }
        if (p != nullptr) {
            p->deleted_flag = true;
        }
        deletedNum++;
        if (deletedNum > theSize / 2) {
            rebuild();
        }
    }

    void rebuild() {
        Node *p = head;
        while (p->next != nullptr) {
            if (p->next->deleted_flag) {
                deleteNode(p, p->next);
            } else {
                p = p->next;
            }
        }
        deletedNum = 0;
    }

    void push_front(Object x) {
        Node *newNode = new Node(x, head->next);
        head->next = newNode;
        ++theSize;
    }

    bool isEmpty() const { return theSize == 0; }

    class const_iterator {
    public:
        const_iterator() : current(nullptr) {}
        const Object &operator*() const { return retrieve(); }
        const_iterator &operator++() {
            current = current->next;
            while (current != nullptr && current->deleted_flag) {
                current = current->next;
            }
            return *this;
        }
        const_iterator operator++(int) {
            const_iterator old = *this;
            ++(*this);
            return old;
        }
        bool operator==(const const_iterator &rhs) const { return current == rhs.current; }
        bool operator!=(const const_iterator &rhs) const { return !(*this == rhs); }

    protected:
        Node *current;
        Object &retrieve() const { return current->data; }
        const_iterator(Node *p) : current(p) {}
        friend class LazyList<Object>;
    };

    const_iterator begin() const { return const_iterator(head->next); }
    const_iterator end() const { return const_iterator(nullptr); }

    void traverse_all_node() {
        Node *p = head->next;
        while (p != nullptr) {
            cout << p->data << " ";
            p = p->next;
        }
        cout << endl;
    }

private:
    Node *head;
    int theSize;    
    int deletedNum;
};


int main() {

    LazyList<int> list;
    for (int i = 0; i < 10; ++i) {
        list.push_front(i);
    }
    
    list.lazyDelete(3);
    list.lazyDelete(5);
    list.lazyDelete(7);
    list.lazyDelete(9);

    cout << "show with out lazy deleted node: " << endl;
    for (auto &x : list) {
        cout << x << " ";
    }
    cout << endl;


    cout << "show with all node: " << endl;
    list.traverse_all_node();

    list.lazyDelete(2);
    list.lazyDelete(4);

    cout << "show with out lazy deleted node: " << endl;
    for (auto &x : list) {
        cout << x << " ";
    }
    cout << endl;

    cout << "show with all node: " << endl;
    list.traverse_all_node();

    return 0;
}