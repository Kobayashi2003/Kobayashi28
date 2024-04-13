#include<iostream>

// 本练习用于演示 protected的使用

using namespace std;

class base {
private :
    int _data1;
protected :
    int _data2;
public :
    int _data3;
    base(int data1 = 1, int data2 = 2, int data3 = 3) : _data1(data1), _data2(data2), _data3(data3) {};
    ~base() {};
};

class derived : public base {
public :
    void show() {
        // cout << _data1 << endl; // erro
        cout << _data2 << endl;
        cout << _data3 << endl;
    }
};

int main() {
    derived d;
    d.show();
    return 0;
}