#ifndef ListNode_h
#define ListNode_h

int allNodes = 0;

struct ListNode
{
    int val = 0;
    ListNode *next = nullptr;
    ListNode(int x = 0) : val(x) {++allNodes;}
};

#endif
