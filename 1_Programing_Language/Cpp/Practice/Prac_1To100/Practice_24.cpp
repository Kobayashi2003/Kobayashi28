#include<iostream>

using namespace std;

namespace mySpace {
    int data;
    void function() {
        cout << "OUT 1" << endl;
    }
    namespace myAnotherSpace { // 名称空间也可以进行嵌套
        int data;
    }
}

int data;

void function() {
    cout << "OUT 2" << endl;
}

int main() {
    :: data = 1;
    mySpace :: data = 2;

    cout << :: data << endl;
    cout << mySpace :: data << endl;
    function();
    :: function();
    mySpace :: function();

    mySpace :: myAnotherSpace :: data = 3;
    cout << mySpace :: myAnotherSpace :: data << endl;

    return 0;
}