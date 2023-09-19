#include<iostream>
#include<iomanip>
#include<cmath>
#include<string>
#include<cstring>
#include<cstdlib>
#include<climits>
#include<ctime>
#include<vector>
#include"answer.h" 
#include"ListNode.h" 

using namespace std;


int main(){
 ListNode* head=new ListNode(0);
 ListNode* abc=head;
 for(int i=1;i<=20;++i){
  ListNode* temp=new ListNode(i);
  abc->next = temp;
  abc=abc->next;
 }
 abc=reverseList(head);
 
 for(int i=1;i<=20;++i){
  cout<<abc->val<<endl;
  abc=abc->next;
 }
 return 0;
}

