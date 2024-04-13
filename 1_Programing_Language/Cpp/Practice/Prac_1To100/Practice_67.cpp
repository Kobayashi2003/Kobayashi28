// A test about Shift Operation in C\C++

#include <iostream>

using std::cout;

void fun1() {
    int a = -1;
    uint32_t b = 0;
    if (a < b) {
        cout << "a < b" << std::endl;
    } else {
        cout << "a >= b" << std::endl;
    }
    // the result is a >= b, cause a is signed int, b is unsigned int
    // when a < b, the result actually is a + 2^32 < b acroding to the rule of shift operation
}

void fun2(int a = -1) {
    cout << (unsigned int)a << std::endl; // the result is 2^32 - 1 
    cout << ~a << std::endl; // the result is 0
    cout << (~(unsigned int)a) + 1 << std::endl; // the result is 1 
}

int main() {
    fun1();
    fun2();    
    return 0;
}