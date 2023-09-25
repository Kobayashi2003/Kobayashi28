#include<iostream>

using namespace std;

class base {
private :
    int _data;
public :
    base(int data = 0) {
        cout << "base construtor work" << endl;
        _data = data;
    }
    ~base() {
        cout << "base destructor work" << endl;
    }
    void showBase() {
        cout << "base: " << _data << endl;
    }
};

class derived : public base {
private :
    int _data2;
public :
    derived(int data2 = 0, int data = 0) : base(data) {
        _data2 = data2;
        cout << "derived construtor work" << endl;
    }
    ~derived() {
        cout << "derived destructor work" << endl;
    }
    void showDerived() {
        cout << "derived: " << _data2 << endl;
    }
};

int main() {

    derived classy(1,2);
    classy.showBase();
    classy.showDerived();
    return 0;
}