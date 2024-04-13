#include<iostream>
#include<string>

// 本练习主要用于演示状态成员的使用

using namespace std;

class A {
private :
    enum Mode {Mode1, Mode2};
    int _data1;
    string _data2;
    Mode _mode;
public :
    A(int data1) {
        _data1 = data1;
        _mode = Mode1;
    }
    A(string data2) {
        _data2 = data2;
        _mode = Mode2;
    }
    A() {
        _data1 = 0;  _data2 = "Hello World !"; _mode = Mode1;
    }
    ~A() {};

    void changeMode() {
        if(_mode == Mode1) {
            _mode = Mode2;
        } else {
            _mode = Mode1;
        }
    }
    void show() {
        if(_mode == Mode1) {
            cout << "DATA1: " << _data1 << endl;
        } else {
            cout << "DATA2: " << _data2 << endl;
        }
    }
    void showMode() {
        cout << "Mode: " << _mode << endl;
    }
};

int main() {
    A a(1);
    a.show();
    a = A("DEMAND");
    a.show();
    a.changeMode();
    a.show(); // 可见再赋值并不是单纯改变某一个类成员
    return 0;
}