#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};

Node* removeDuplicateNodes(Node* h);

Node* removeDuplicateNodes(Node* h) {
    vector<int> table;
    Node *cur = h, *pre = nullptr;
    while (cur != nullptr) {
        if (find(table.begin(), table.end(), cur->value) == table.end()) {
            table.push_back(cur->value);
            pre = cur; cur = cur->next;
            continue;
        }
        pre->next = cur->next;
        delete cur;
        cur = pre->next;
    }
    return h;
}