#include <vector>
#include <algorithm>

using namespace std;

struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};

Node* FindKthBigElementInTwoList(Node* List1, Node* List2, int k);

Node* FindKthBigElementInTwoList(Node* List1, Node* List2, int k) {
    vector<int> vec;
    while (List1 != nullptr) {
        vec.push_back(List1->value);
        List1 = List1->next;
    }
    while (List2 != nullptr) {
        vec.push_back(List2->value);
        List2 = List2->next;
    }
    sort(vec.begin(), vec.end());
    return new Node(vec[vec.size() - k]);
}