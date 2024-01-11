#include <iostream>
#include "function.h"

using namespace std;

Node* initList(int n) {
    Node* pre = nullptr;
    Node* head = nullptr;
    int t, data;
    for(int i = 0; i < n; ++i) {
        cin >> t >> data;
        Node* tmp = new Node(t, data);
        if (pre == nullptr) {
            pre = tmp;
            head = pre;
        } else {
            pre->next = tmp;
            tmp->prior = pre;
            pre = pre->next;
        }
    }
    return head;
}

void printList(Node* head) {
	Node* temp = head;
	cout << temp->data;
	temp = temp->next;
	while(temp != nullptr) {
		cout << " " << temp->data;
		temp = temp->next;
	}
	cout << endl;
	
	/*
	temp = head;
	cout << temp->freq;
	temp = temp->next;
	while(temp != nullptr) {
		cout << " " << temp->freq;
		temp = temp->next;
	}
	cout << endl;
	*/

}

int main() {
    int n;
    cin >> n;
    //初始化List
    Node* head = initList(n);
	
	head = Locate(head, 1);
	printList(head);
	head = Locate(head, 1);
	printList(head);
	head = Locate(head, 1);
	head = Locate(head, 1);
	head = Locate(head, 1);
	printList(head);
	
}