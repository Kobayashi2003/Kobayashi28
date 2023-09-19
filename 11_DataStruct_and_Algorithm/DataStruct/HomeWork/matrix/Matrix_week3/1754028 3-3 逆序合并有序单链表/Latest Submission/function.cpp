#include "function.h"
/*
2 5 6 8 9
1 3 4 7
*/

Node* ReverseList(Node* head) {
    Node* temp = head;
    Node* temp_parent = temp;
    Node* temp_next = temp->next;
    while (temp_next!=nullptr) {
        temp = temp_next;
        temp_next = temp->next;
        temp->next = temp_parent;
        temp_parent = temp;
    } 
    head->next = nullptr;
    return temp;
}

Node* ReverseMergeList(Node* List1, Node* List2) {
    Node* l1_ptr = List1;
    Node* l2_ptr = List2;
    Node* temp = new Node(-1);
    Node* head = temp;
    while (l1_ptr!=nullptr&&l2_ptr!=nullptr){
        if (l1_ptr->value<l2_ptr->value) {
            temp->next = new Node(-1);
            temp = temp->next;
            temp->value = l1_ptr->value;
            l1_ptr = l1_ptr->next;
            
        } else {
            temp->next = new Node(-1);
            temp = temp->next;
            temp->value = l2_ptr->value;
            l2_ptr = l2_ptr->next;
        }
    }
    while (l1_ptr!=nullptr) {
        temp->next = new Node(-1);
        temp = temp->next;
        temp->value = l1_ptr->value;
        l1_ptr = l1_ptr->next;
    }
    while (l2_ptr!=nullptr) {
        temp->next = new Node(-1);
        temp = temp->next;
        temp->value = l2_ptr->value;
        l2_ptr = l2_ptr->next;
    }
    temp = head->next;
    delete head;
    head = nullptr;
    return ReverseList(temp);
}
