#include<iostream>

using namespace std;

class A {
    private :
        int data;
    public :
        A() {
            cout << "A default constructor work" << endl;
            data = 0;
        }
        A(int data) {
            cout << "A constructor work" << endl;
            A :: data = data;
        }
        A(A &a) {
            cout << "A copy constructor work" << endl;
            data = a.data;
        }
        ~A() {
            cout << "A destructor work" << endl;
        }
};

class B {
    private :
        int *pdata;
    public :
        B() {
            cout << "B default constructor work" << endl;
            pdata = NULL;
        }
        B(int *pdata) {
            cout << "B constructor work" << endl;
            B :: pdata = new int();
            *(B :: pdata) = *pdata;
        }
        B(B &b) {
            cout << "B copy constructor work" << endl;
            pdata = new int();
            *(pdata) = *(b.pdata);
        }
        ~B() {
            cout << "B distructor work" << endl;
            if(pdata) {
                delete pdata;
            }
        }
        B & operator = (B &b) {
            cout << "B copy assignment operator work" << endl;
            if(pdata) {
                delete pdata;
            }
            if(b.pdata) {
                pdata = new int();
                *(pdata) = *(b.pdata);
            } else {
                pdata = NULL;
            }
            return *this;
        }
};

int main() {
    int data = 1;

    A a1;
    A a2(data);
    A a3 = a2;
    A a4(a3);

    B b1;
    B b2(&data);
    B b3 = b2;
    B b4(b3);
    return 0;
}

// 输出结果：
// A default constructor work
// A constructor work
// A copy constructor work
// A copy constructor work

// B default constructor work
// B constructor work
// B copy constructor work // 由此可见，拷贝构造函数与=重载同时存在时，编译器将会选择调用拷贝构造函数
// B copy constructor work

// B distructor work
// B distructor work
// B distructor work
// B distructor work
// A destructor work
// A destructor work
// A destructor work
// A destructor work