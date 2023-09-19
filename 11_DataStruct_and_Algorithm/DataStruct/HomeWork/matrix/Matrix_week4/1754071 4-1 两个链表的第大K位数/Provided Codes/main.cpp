#include "function.h"
#include <iostream>
#include <vector>
using namespace std;
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
    vector<int> input1(5);
    for (int i = 0; i < 5; i++) {
        cin >> input1[i];
    }
    vector<int> input2(5);
    for (int i = 0; i < 5; i++) {
        cin >> input2[i];
    }
    Node* list1 = addList(input1);
    Node* list2 = addList(input2);
    Node* kthBigElement = FindKthBigElementInTwoList(list1,list2,7);
    cout << kthBigElement->value <<" ";
	cin >> input1[0];
	return 0;
}