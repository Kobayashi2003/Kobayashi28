#include<iostream>

using namespace std;

class A {
public :
    A() {
        cout << "A create" << endl;
    };
    virtual ~A() {
        cout << "A delete" << endl;
    }

    void function1() {
        cout << "A: fun1" << endl;
    }
    virtual void function2() {
        cout << "A: fun2" << endl;
    }
    virtual void function3() = 0;
};

class B : public A {
public :
    B() {
        cout << "B create" << endl;
    };
    virtual ~B() {
        cout << "B delete" << endl;
    };

    void function1() {
        cout << "B: fun1" << endl;
    }
    virtual void function2() {
        cout << "B: fun2" << endl;
    }
    virtual void function3() {
        cout << "B: fun3" << endl;
    }
};

int main() {

    B b1;
    b1.function1();
    b1.function2();
    b1.function3();

    B *b2 = new B();
    b2 -> function1();
    b2 -> function2();
    b2 -> function3();

    A *b3 = new B();
    b3 -> function1();
    b3 -> function2();
    b3 -> function3();
    return 0;
}