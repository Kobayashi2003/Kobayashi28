#ifndef HAS_CYCLE_H_
#define HAS_CYCLE_H_

#include <vector>
using namespace std;

 struct ListNode {
     int val;
     ListNode *next;
     ListNode(int x) : val(x), next(nullptr) {}
 };

bool hasCycle(ListNode *head);

#endif // !HAS_CYCLE_H_