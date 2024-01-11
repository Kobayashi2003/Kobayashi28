#include "function.h"

Node* Locate(Node* head, int x) {
	Node *p = head;
	while(p != nullptr) {
		//寻找data为x的节点,称为目标节点
		if(p->data == x) {
			p->freq ++;
			//若目标节点是头结点，或目标节点的freq小于等于其prior节点，不需要调整位置
			if(p->prior == nullptr || p->freq <= p->prior->freq) {
				return head;
			} 
			else {
				//从链表中剔除目标节点
				if(p->next != nullptr) {
					p->next->prior = p->prior;
				}
				p->prior->next = p->next;
			}
			
			//将目标节点插入到新的位置
			Node *temp = p->prior;
			while(temp != nullptr) {
				//从目标节点p向前搜索，找到第一个freq大于等于p->freq的节点temp（即p要插入到temp后）
				if(temp->freq >= p->freq) {
					//将p插入到temp后面
					temp->next->prior = p;
					p->next = temp->next;
					p->prior = temp;
					temp->next = p;
					return head;	
				}
				else {
					temp = temp->prior;
				}
			}
			// temp==nullptr,说明p->freq在所有节点中最大,即p是新的头结点
			p->next = head;
			p->prior = nullptr;
			head->prior = p;
			head = p;
			return head;
		}
		else {
			p = p->next;
		}
	}
	return head;
}

