#include "helper.h"

Node* GetLastNode(Node* head) {
    Node* temp = head;
    Node* temp_parent = temp;
    while (temp!=nullptr){
        temp_parent = temp;
        temp = temp->next;
    }
    return temp_parent;
}
//-1 1 2
Node* addList(vector<int> data) {
    vector<Node*> nodes;
    for (int i = 0; i < data.size(); i++) {
        Node* temp = new Node(data[i]);
        nodes.push_back(temp);
    }
    for (int i = 0; i < nodes.size()-1; i++) {
        nodes[i]->next=nodes[i+1];
    }
    return nodes[0];
}
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