#include <iostream>
#include <vector>
using namespace std;

struct Node{
	Node* prior;
    Node* next;
    int data;
    int freq;
    Node(int val, int fre):data(val),freq(fre),prior(nullptr),next(nullptr){}
};

Node* Locate(Node* head, int x);