#include<iostream>

using namespace std;

class A {
private :
    enum {LEN = 10};
    int _data[LEN]; // 注意，用这种方式声明枚举并不会创建类数据成员，也就是说，所有的对象中都不包含枚举
    // LEN在此处只是一个符号名称，在作用域为整个类的代码中遇到它时，编译器将会自动用10替代它
    // 由于这里使用枚举只是为了创建符号常量，并不打算创建枚举变量，因此不需要为它提供枚举名
public :
    A(int data = 0) {
        for(int i = 0; i < LEN; ++i) {
            _data[i] = data;
        }
    }
    ~A() {}
};

int main() {
    A a;
    return 0;
}