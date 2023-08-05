#include<iostream>

using namespace std;


// 队列类
// 1. 队列存储有序的项目序列
// 2. 队列能够容纳的项目数有一定的限制
// 3. 应当能够创建空队列
// 4. 应当能够检查队列是否为空
// 5. 应当能够检查队列是否为满
// 6. 应当能够在队尾添加项目
// 7. 应当能够在队首删除项目
// 8. 应当能够确定队列中的项目数
template <typename Type>
class Queue {
private :
    enum {MAX = 10};
    struct Node {
        Type item;
        struct Node * next;
    };

    Node * front; // pointer to front of Queue
    Node * rear; // pointer to back of Queue
    int items; // current number of items in Queue
    const int qsize; // maximum number of items in Queue
public :
    Queue(int size = MAX);
    ~Queue();
    bool isempty() const;
    bool isfull() const;
    int queuecount() const;
    bool enqueue(); // add item to end
    bool dequeue(); // remove item from front
};

template <typename Type>
Queue<Type>::Queue(int size) : front(nullptr), rear(nullptr), items(0), qsize(size) {

    cout << "Queue constructor work" << endl;

    rear = new Node();
    rear -> next = nullptr;
    Node * node = rear;
    for(int i = 0; i < qsize - 1; ++i) {
        Node * newNode = new Node();
        newNode -> next = nullptr;
        node -> next = newNode;
        node = newNode;
    }
    front = node;

    cout << "Queue constructor end" << endl;
}

template <typename Type>
Queue<Type>::~Queue() {
    cout << "Queue destructor work" << endl;

    for(auto p1 = rear, p2 = rear -> next; p2 != nullptr; p1 = p2, p2 = p1 -> next) {
        delete p1;
    }
    delete front;

    cout << "Queue constructor end" << endl;
}

int main() {
    Queue <int> q;
    return 0;
}