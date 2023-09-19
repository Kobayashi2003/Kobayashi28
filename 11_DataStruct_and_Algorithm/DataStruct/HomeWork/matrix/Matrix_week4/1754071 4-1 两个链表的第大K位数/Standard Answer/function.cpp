#include "function.h"
#include <algorithm>

// 输入：
// 7
// 7 3 5 9 2	
// 8 1 6 10 4
// 输出
// 4
bool cmp(Node* a, Node* b) {
    return a->value>b->value;
}

Node* FindKthBigElementInTwoList(Node* List1, Node* List2, int k) {
    vector<Node*> array;
    Node* temp = List1;
    while (temp!=nullptr) {
        array.push_back(temp);
        temp = temp->next;
    }
    temp = List2;
    while (temp!=nullptr) {
        array.push_back(temp);
        temp = temp->next;
    }
    sort(array.begin(),array.end(),cmp);
    return array[k-1];
}

