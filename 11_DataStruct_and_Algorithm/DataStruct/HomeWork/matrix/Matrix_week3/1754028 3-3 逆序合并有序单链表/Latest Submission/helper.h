#include <vector>
#ifndef helper
#define helper
using namespace std;
struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};
Node* addList(vector<int> data);
Node* ReverseList(Node* head);
Node* GetLastNode(Node* head);
#endif