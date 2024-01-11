#include<iostream>
#include<stdlib.h>
#include<queue>

template<typename eT>
class node {
public:
	eT data;
	node* next;
	node(const eT& data_, node<eT>* next_ = NULL)
	{
		data = data_;
		next = next_;
	}
	node() : next(NULL) {}
	~node() {}
};

template<typename eT>
class linkQueue :public std::queue<eT> {
public:
	node<eT>* front, * tail;
public:
	linkQueue() { front = tail = NULL; }
	~linkQueue() {
		node<eT>* tmp;
		while (front != NULL) {
			tmp = front;
			front = front->next;
			delete tmp;
		}
	}
	bool isEmpty() { return front == NULL; }
	void enQueue(const eT& x) {
		if (tail == NULL)
			front = tail = new node<eT>(x);
		else {
			tail->next = new node<eT>(x);
			tail = tail->next;
		}
	}
	eT deQueue() {
		node<eT>* tmp = front;
		eT value = front->data;
		front = front->next;
		if (front == NULL) tail = NULL;
		delete tmp;
		return value;
	}
};

template <typename eT>
class priorityQueue :public linkQueue<eT>
{
public:
	void enQueue(const eT& x)
	{
		node<eT> *newNode = new node<eT>(x);
		node<eT> *p = this->front;
		if (this->tail == nullptr) {
			this->front = this->tail = newNode;
			return;
		}
		while (p->next != nullptr && p->next->data < x) p = p->next;
		newNode->next = p->next;
		p->next = newNode;
		if (p == this->tail) this->tail = newNode;
	}
};

class simulator {
	int noOfServer;
	int customNum;
	int* arrivalTimeList;
	int* serviceTimeList;
	struct eventT
	{
		int time; //事件发生时间
		int type; //事件类型。0 为到达，1 为离开
		bool operator<(const eventT& e) const { return time < e.time; }
	};
public:
	simulator() {
		//std::cout << "请输入柜台数：";
		std::cin >> noOfServer;
		//std::cout << "请输入模拟的顾客数：";
		std::cin >> customNum;
		arrivalTimeList = new int[customNum];
		serviceTimeList = new int[customNum];
		for (int i = 0; i < customNum; i++) {
			std::cin >> arrivalTimeList[i];
		}
		for (int i = 0; i < customNum; i++) {
			std::cin >> serviceTimeList[i];
		}
	}
	~simulator() {
		delete arrivalTimeList;
		delete serviceTimeList;
	}
	int avgWaitTime() {
		int serverBusy = 0;
		int serviceTime = 0;
		int currentTime = 0;
		int totalWaitTime = 0;
		linkQueue<eventT> waitQueue;
		priorityQueue<eventT> customerQueue;
		linkQueue<int> serviceTimeQueue;
		eventT currentEvent;
		//生成初始的事件队列
		int i;
		for (i = 0; i < customNum; ++i)
		{
			currentEvent.type = 0;
			currentTime = arrivalTimeList[i];//每个顾客的到达时刻
			currentEvent.time = currentTime;
			customerQueue.enQueue(currentEvent);
			serviceTimeQueue.enQueue(serviceTimeList[i]);//每个顾客的服务时间
		}
		while (!customerQueue.isEmpty())
		{
			currentEvent = customerQueue.deQueue();
			currentTime = currentEvent.time;
			switch (currentEvent.type)
			{
			case 0:
				if (serverBusy < noOfServer) {
					++serverBusy;
					currentEvent.type = 1;
					serviceTime = serviceTimeQueue.deQueue();
					currentEvent.time = currentTime + serviceTime;
					customerQueue.enQueue(currentEvent);
				}
				else {
					waitQueue.enQueue(currentEvent);
				}
				break;

			case 1:
				--serverBusy;
				if (!waitQueue.isEmpty()) {
					++serverBusy;
					currentEvent = waitQueue.deQueue();
					currentEvent.type = 1;
					serviceTime = serviceTimeQueue.deQueue();
					totalWaitTime += currentTime - currentEvent.time;
					currentEvent.time = currentTime + serviceTime;
					customerQueue.enQueue(currentEvent);
				}
				break;
			}
		}
		return totalWaitTime / customNum;
	}
};
int main()
{
	simulator sim;
	std::cout << sim.avgWaitTime() << std::endl;
	return 0;
}