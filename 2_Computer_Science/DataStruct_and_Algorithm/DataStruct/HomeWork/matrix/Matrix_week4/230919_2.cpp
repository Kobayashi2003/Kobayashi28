#include <iostream>
#include <vector>
using namespace std;

struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};

Node* insert(Node* head, int insertVal);

Node* insert(Node* head, int insertVal) {
    if (head == nullptr) {
        head = new Node(insertVal);
        head->next = head;
        return head;
    }
    Node* cur = head;
    while (cur->next != head) {
        if (cur->value <= insertVal && cur->next->value >= insertVal) {
            break;
        }
        if (cur->value > cur->next->value && (cur->value <= insertVal || cur->next->value >= insertVal)) {
            break;
        }
        cur = cur->next;
    }
    Node* insertNode = new Node(insertVal);
    insertNode->next = cur->next;
    cur->next = insertNode;
    return head;
}