#include<iostream>

using namespace std;

void function(int data) {
    cout << data << endl;
}

int main() {
    void function(int data = 1); // 通过函数原型设置data的默认值为 1
    function();
    function(2);
    return 0;
}