#include<iostream>

using namespace std;

class base {
private :
    int _data1;
public :
    base(int data = 1)  {
        cout << "constructor1 work" << endl;
        _data1 = data;
    }
    virtual ~base() {
        cout << "destructor work: " << "" << this << endl;
    }
    virtual void show() {
        cout << "data1: " << _data1 << endl;
    }
};

class derived : public base {
private :
    int _data2;
public :
    derived(int data1 = 1, int data2 = 2) : base(data1) {
        cout << "constructor2 work" << endl;
        _data2 = data2;
    }
    virtual void show() {
        cout << "data2: " << _data2 << endl;
    }
};

int main() {
    cout << "test point 1" << endl;
    base b;
    cout << "test point 2" << endl;
    derived d;
    cout << "test point 3" << endl;
    b.show();
    d.show();
    cout << "test point 4" << endl;
    cout << "base: " << &b << endl;
    cout << "derived: " << &d << endl;
    cout << "test point 5" << endl;
    return 0;
}