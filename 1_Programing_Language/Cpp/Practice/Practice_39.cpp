#include<iostream>

// 本练习主要用于解答为什么复制构造函数参数要使用引用值

using namespace std;

class A {
public :
    A() {
        cout << "constructor work" << endl;
    }
    ~A() {
        cout << "               destructor work" << endl;
    }
    A(const A& a) {
        cout << "       copy construct work" << endl;
    }
    void myFun1(A &a) {
        cout << "   myFun1 work" << endl;
    }
    void myFun2(A a) {
        cout << "   myFun2 work" << endl;
    }
    void operator=(A &a){
        cout << "= overloaded function work" << endl;
    }
};

int main() {
    A a1, a2;
    a1.myFun1(a2);
    a1.myFun2(a2);
    return 0;
}

// result：

// constructor work
// constructor work
//    myFun1 work
//        copy construct work   // 从最后的结果中可看出：在调用myFun2之前，
                                // 程序调用了一次复制构造函数，这是因为myFun的参数使用的不是引用类型，因此在传参的过程中，
                                // 系统将会隐式地调用复制构造函数生成一个临时对象，
                                // 然后将值复制到该临时对象中供函数使用
//    myFun2 work
//                destructor work
//                destructor work
//                destructor work


// 由此可知，若复制构造函数中的参数并非引用值，那么将会出现对复制构造函数无终止的递归调用的状况，这是不允许发生的