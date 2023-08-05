// 委托构造函数（delegoting constructors）

#include <iostream>

class Test {
public:
    Test(int n) {}

    Test() : Test(0) {} // delegating constructor
};

int main() { return 0; }
