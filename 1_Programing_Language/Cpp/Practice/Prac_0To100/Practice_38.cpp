#include<iostream>

using namespace std;

class Num {
private :
    int _data;
public :
    Num(int data = 0) {
        _data = data;
    }
    ~Num() {}
    operator int() const {
        cout << "conversion function work" << endl;
        return _data;
    }
    // 非友元的重载版本
    Num & operator+(Num & num) {
        cout << "overed function work" << endl;
        _data += num._data;
        return *this;
    }
    // 友元的重载版本
    friend int operator-(Num & num1, Num & num2) {
        return num1._data - num2._data;
    }
};

int main() {

    Num num1(10);
    Num num2(11);
    cout << num1 + num2 << endl;
    cout << num2 - num1 << endl;
    return 0;
}