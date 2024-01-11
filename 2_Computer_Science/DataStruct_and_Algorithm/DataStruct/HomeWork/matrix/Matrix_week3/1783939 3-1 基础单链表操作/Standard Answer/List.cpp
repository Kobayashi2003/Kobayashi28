#include "List.h" 
Node* List::SearchkthNode(int k) {
    Node* temp = head;
    Node* result = nullptr;
    int cnt = 0;
    while (temp != nullptr) {
        cnt += 1;
        if (cnt == k) {
            result = temp;
            break;
        }
        if (temp->next != nullptr) {
            temp = temp->next;
        }
    }
    return result;
}
void List::InsertBack(Node* n){
    if (n != nullptr) {
        Node* temp = head;
		if (temp == nullptr) {
			head = n;
		}
		else {
			while (temp->next != nullptr) {
				temp = temp->next;
			}
			temp->next = n;
			n->next = nullptr;
		}
    }
}
void List::DeleteElement(int k) {
    int cnt = k-1;
    Node* temp = head;
    Node* temp_parent = temp;
    if (k == 1) {
        head = head->next;
        delete temp;
        temp = nullptr;
    } else {
        while (cnt > 0) {
            if (temp!=nullptr) {
                cnt = cnt - 1;
                temp_parent = temp;
                temp = temp->next;
            } else{
                break;
            }
        }
        if (cnt==0) {
            temp_parent->next = temp->next;
            delete temp;
            temp = nullptr;
        } 
    }
}
void List::InsertAfterKth(Node* n, int k) {
    int cnt = k-1;
    Node* temp = head;
    if (k == 0) {
        head = n;
        head->next = temp;
    } else {
        while (cnt>0) {
            if (temp!=nullptr) {
                cnt = cnt - 1;
                temp = temp->next;
            } else{
                break;
            }
        }
        if (cnt==0) {
            n->next = temp->next;
            temp->next = n; 
        } 
    }
}