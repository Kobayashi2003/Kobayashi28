// 本练习目的在于熟悉const成员函数的定义以及观察它在重载解析中的优先级

#include<iostream>

using namespace std;

class A {
private :
    int _data;
public :
    A(int data) {
        _data = data;
    }
    ~A() {}
    void show() const { // 若无const该成员函数,a在调用show()函数时将会报错,这是因为程序将无法保证show()函数的代码不会改变对象中的值
        cout << "OUT1: " << _data << endl;
    }
    void show() { // 若无该成员函数,程序仍然能够正常运行,说明非const的对象也能够调用const成员函数
        cout << "OUT2: " << _data << endl;
    }
};

int main() {
    const A a(1);
    A b(2);
    a.show();
    b.show();
    return 0;
}