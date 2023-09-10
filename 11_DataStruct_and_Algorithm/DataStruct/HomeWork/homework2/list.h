#ifndef LIST_H
#define LIST_H

template <typename Comparable>
struct ListNode {
    Comparable data;
    ListNode *next;
};


template <typename Comparable>
struct HeadNode : public ListNode<Comparable> {};


template <typename Comparable>
class List {
public: // public values
    int size;
    HeadNode<Comparable> *head;

public: // constructor and destructor
    List() {
        head = new HeadNode<Comparable>;
        head->next = nullptr;
        size = 0;
    }
    ~List() {
        ListNode<Comparable> *preNode, curNode;
        preNode = head; curNode = head->next;
        while (curNode != nullptr) {
            delete preNode;
            preNode = curNode;
            curNode = curNode->next;
        }
        delete preNode;
    }

public: // public methods 
    int ListLength() const { return size; }
    void OrderInsert(const Comparable &x);   
    void DelRepeat();
    void DelReapeat(int);
    void DelRange(const Comparable &min, const Comparable &max);

public: // static methods
    static HeadNode<Comparable> * Merge(List<Comparable> &list1, List<Comparable> &list2);
};


template <typename Comparable>
void List<Comparable>::OrderInsert(const Comparable &x) {
    ListNode<Comparable> *preNode, *curNode;
    preNode = head; curNode = head->next;
    while (curNode != nullptr && curNode->data < x) {
        preNode = curNode;
        curNode = curNode->next;
    }
    ListNode<Comparable> *newNode = new ListNode<Comparable>;
    newNode->data = x;
    newNode->next = curNode;
    preNode->next = newNode;
    ++size;
}


template <typename Comparable>
void List<Comparable>::DelRepeat() {
    // if the list is increamentally ordered
    ListNode<Comparable> *preNode, *curNode;
    preNode = head; curNode = head->next;
    while (curNode != nullptr) {
        if (curNode->data == preNode->data) {
            preNode->next = curNode->next;
            delete curNode;
            curNode = preNode->next;
            --size;
        } else {
            preNode = curNode;
            curNode = curNode->next;
        }
    }
}


template <typename Comparable>
void List<Comparable>::DelReapeat(int) {
    // if the list is randomly ordered
    ListNode<Comparable> *preNode, *curNode;
    preNode = head; curNode = head->next;
    Comparable *table = new Comparable[size];
    int count = 0;

    auto checkRepeat = [&table, &count](const Comparable &x) {
        for (int i = 0; i < count; ++i)
            if (table[i] == x) return true;
        return false;
    };

    while (curNode != nullptr) {
        if (checkRepeat(curNode->data)) {
            preNode->next = curNode->next;
            delete curNode;
            curNode = preNode->next;
            --size;
        } else {
            table[count++] = curNode->data;
            preNode = curNode;
            curNode = curNode->next;
        }
    }

    delete [] table;
}


template <typename Comparable>
void List<Comparable>::DelRange(const Comparable &min, const Comparable &max) {
    ListNode<Comparable> *preNode, *curNode;
    preNode = head; curNode = head->next;
    while (curNode != nullptr) {
        if (curNode->data >= min && curNode->data <= max) {
            preNode->next = curNode->next;
            delete curNode;
            curNode = preNode->next;
            --size;
        } else {
            preNode = curNode;
            curNode = curNode->next;
        }
    }
}


template <typename Comparable>
HeadNode<Comparable> * List<Comparable>::Merge(List<Comparable> &list1, List<Comparable> &list2) {
    HeadNode<Comparable> *head1, *head2, *head3;
    head1 = list1.head; head2 = list2.head;
    head3 = new HeadNode<Comparable>;
    head3->next = nullptr;

    ListNode<Comparable> *p1, *p2;
    p1 = head1->next; p2 = head2->next;
    while (p1 != nullptr || p2 != nullptr) {
        if (p1->data < p2->data) {
            ListNode<Comparable> *newNode = new ListNode<Comparable>;
            newNode->data = p1->data;
            newNode->next = head3->next;
            head3->next = newNode;
            p1 = p1->next;
        } else {
            ListNode<Comparable> *newNode = new ListNode<Comparable>;
            newNode->data = p2->data;
            newNode->next = head3->next;
            head3->next = newNode;
            p2 = p2->next;
        }
    }
    if (p1 != nullptr) {
        ListNode<Comparable> *newNode = new ListNode<Comparable>;
        newNode->data = p1->data;
        newNode->next = head3->next;
        head3->next = newNode;
        p1 = p1->next;
    } else if (p2 != nullptr) {
        ListNode<Comparable> *newNode = new ListNode<Comparable>;
        newNode->data = p2->data;
        newNode->next = head3->next;
        head3->next = newNode;
        p2 = p2->next;
    }

    return head3;
}

#endif // LIST_H