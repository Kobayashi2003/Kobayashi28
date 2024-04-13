// 基于堆对象的链表结构

#include<iostream>
#include<vector>

#define dataSize 10

using namespace std;

typedef int dataType;

int count1 = 0, count2 = 0;

class Node {
    private :
        Node *p;
        dataType data;
    public :
        Node(Node *p, dataType data) {
            Node :: p = p;
            Node :: data = data;
            cout << "Constructor work: " << count1++ << endl;
        }
        ~Node() {
            cout << "NUMBER" << data << endl;
            cout << "Destructor work: " << count2++ << endl;
        }
        void connect(Node *newNode) {
            p = newNode;
            cout << "Connected" << endl;
        }
        void show() {
            cout << "show the data: " << data << endl;
            if(p != NULL) {
                p -> show();
            }
        }
        void distory() {
            if(p != NULL) {
                p -> distory();
            }
            delete this;
        }
};


int main() {
    vector <dataType> data;
    data.resize(dataSize);
    for(int i = 0; i < dataSize; i++) {
        data[i] = i;
    }

    Node *head = new Node(NULL, -1);
    Node *node = head;
    for(unsigned int i = 0; i < data.size(); ++i) {
        Node *newNode = new Node(NULL, data[i]);
        node -> connect(newNode);
        node = newNode;
    }

    head -> show();
    head -> distory();

    return 0;
}