#include <iostream>
#include <vector>
using namespace std;

struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};

Node* insert(Node* head, int insertVal);