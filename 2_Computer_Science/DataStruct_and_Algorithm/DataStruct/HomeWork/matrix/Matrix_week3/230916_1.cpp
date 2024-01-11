#include <iostream>
#include <vector>
using namespace std;

struct Node{
    int value;
    Node* next;
    Node(int val):value(val),next(nullptr){}
};

class List{
public:
    Node* head;
    List() {
        head = nullptr;
    }
public:
    void InsertBack(Node* n);
    void InsertAfterKth(Node* n, int k);
    void DeleteElement(int k);
    Node* SearchkthNode(int k);
};

Node* List::SearchkthNode(int k) {
    Node * p = head;
    for (int i = 0; i < k-1; ++i) {
        if (p == nullptr)
            return nullptr;
        p = p->next;
    }
    return p;
}

void List::InsertBack(Node * n) {
    if (head == nullptr) {
        head = n;
        return ;
    }
    Node *p = head;
    while (p->next != nullptr) 
        p = p->next;
    p->next = n; 
}

void List::InsertAfterKth(Node* n, int k) {
    if (k == 0) {
        n->next = head;
        head = n;
        return ;
    }
    Node *p = head;
    for (int i = 1; i < k; i++) 
        p = p->next;
    n->next = p->next;
    p->next = n;
}

void List::DeleteElement(int k) {
    if (k == 1) {
        Node * delNode = head;
        head = head->next;
        delete delNode;
        return ;
    }
    Node *p = head;
    for (int i = 1; i < k-1; ++i)
        p = p->next;
    Node * delNode = p->next;
    p->next = p->next->next;
    delete delNode;
}

vector<int> printList(Node* head) {
    vector<int> result;
    Node* temp = head;
    if (temp == nullptr) {
        result.push_back(-1);
    }
    while (temp!=nullptr) {
        result.push_back(temp->value);
        temp = temp ->next;
    }
    return result;
}


int main() {
    vector<int> input(6); // input size = 6
    for (int i = 0; i < 6; i++) {
        cin >> input[i];
    }
    List list;
    list.InsertBack(new Node(input[0]));
    list.InsertBack(new Node(input[1]));
    list.InsertBack(new Node(input[2]));
    list.InsertAfterKth(new Node(input[3]),0);
    list.InsertAfterKth(new Node(input[4]),1);
    list.InsertAfterKth(new Node(input[5]),5);
    vector<int> result1 = printList(list.head);
    for (int i = 0; i < 6; i++) {
        cout << result1[i] <<" ";
    }
    cout << endl;
	cout << list.SearchkthNode(1)->value << endl;
    list.DeleteElement(1);
	//5 1 2 3 6
    list.DeleteElement(2);
	//5 2 3 6
    list.DeleteElement(3);
	//5 2 6
    vector<int> result2 = printList(list.head);
    for (int i = 0; i < 3; i++) {
        cout << result2[i] << " ";
    }
    cout << endl;
    list.DeleteElement(1);
    list.DeleteElement(1);
    list.DeleteElement(1);
    if(list.SearchkthNode(1) == nullptr) {
        cout << -1 << endl;
    }
	return 0;
}