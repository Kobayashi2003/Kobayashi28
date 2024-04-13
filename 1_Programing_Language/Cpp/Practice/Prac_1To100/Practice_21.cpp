#include<iostream>
#include<string>

using namespace std;

struct Node {
    int data;
};

void function() {
    cout << "default out" << endl;
}

template <typename T> void function(T &data) {
    cout << "OUT 1: " << data << endl;
}

template <> void function<Node>(Node &node) { // 注意参量的格式
    cout << "OUT 2: " << node.data << endl;
}

int main() {
    Node node;
    node.data = 21;
    function(node);
    int num = 5;
    function(num);
    string str = "Hello World !" ;
    function(str);
    function();
    return 0;
}