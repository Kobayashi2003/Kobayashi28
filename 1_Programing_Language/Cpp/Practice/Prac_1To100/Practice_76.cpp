#include <iostream>

using namespace std;

void fun1() {
    cout << "fun1" << endl;
}

void fun2() {
    cout << "fun2" << endl;
}

void fun3() {
    cout << "fun3" << endl;
}

int main() {

    unsigned short int pattern = 0; cin >> pattern;

    // 000 001 010 011 100 101 110 111
    if (pattern & 1) fun1();
    if (pattern>>1 & 1) fun2();
    if (pattern>>2 & 1) fun3();

    return 0;
}