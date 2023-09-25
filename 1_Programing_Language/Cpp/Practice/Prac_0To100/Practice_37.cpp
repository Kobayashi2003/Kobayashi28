#include<iostream>
// 本练习主要用于展示转换函数的使用形式
using namespace std;

class Length {
private :
    int _length;
public :
    Length(int length = 0) {
        _length = length;
    }
    ~Length() {};
    operator int() const {
        return _length;
    }
};

int main() {
    Length l(15);
    int _l = l;
    cout << _l << endl;
    return 0;
}