#include <iostream>
#include "List.h"

using namespace std;

Node* initList(int n) {
    Node* pre = nullptr;
    Node* h = nullptr;
    int t;
    for(int i = 0; i < n; ++i) {
        cin >> t;
        Node* tmp = new Node(t);
        if (pre == nullptr) {
            pre = tmp;
            h = pre;
        } else {
            pre->next = tmp;
            pre = pre->next;
        }
    }
    return h;
}

int main() {
    int n;
    cin >> n;
    //初始化List
    Node* h = initList(n);
    Node* head;
    head = h;
    
    head = removeDuplicateNodes(head);
    if(head != nullptr)	{
		cout << head->value;
		head = head->next;
	}
	while(head != nullptr) {
		cout << " " << head->value;
		head = head->next;
	}
}