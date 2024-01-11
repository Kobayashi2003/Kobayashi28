#include "List.h"

Node* removeDuplicateNodes(Node* head) {
    Node* ob = head;
    while (ob != nullptr) {
        Node* oc = ob;
        while (oc->next != nullptr) {
            if (oc->next->value == ob->value) {
                oc->next = oc->next->next;
            } else {
                oc = oc->next;
            }
        }
        ob = ob->next;
    }
    return head;
}