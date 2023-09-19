#include "List.h"

Node* insert(Node* head, int insertVal) {
    Node *node = new Node(insertVal);
    if (head == nullptr) {
        node->next = node;
        return node;
    }
    if (head->next == head) {
        head->next = node;
        node->next = head;
        return head;
    }
    Node *curr = head, *next = head->next;
    while (next != head) {
        if (insertVal >= curr->value && insertVal <= next->value) {
            break;
        }
        if (curr->value > next->value) {
            if (insertVal > curr->value || insertVal < next->value) {
                break;
            }
        }
        curr = curr->next;
        next = next->next;
    }
    curr->next = node;
    node->next = next;
    return head;
}

