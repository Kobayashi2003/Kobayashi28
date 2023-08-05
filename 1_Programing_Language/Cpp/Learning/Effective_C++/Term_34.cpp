// Difference between inheritance of interface and inheritance of implementation
// 区分接口继承和实现继承

// 接口及岑和实现继承不同。在 public 继承之下，derived classes 总是继承 base classes 的接口
// pure virtual 函数只具体指定接口继承
// impure virtual 函数具体指定接口接口继承及确省实现继承
// non-virtual 函数具体指定接口继承以及强制性实现继承 

#include <iostream>

class Airport {};

class Airplane {
public:
    virtual void fly(const Airport& destination) = 0;
};

void Airplane::fly(const Airport& destination) {}

class ModelA: public Airplane {
public:
    virtual void fly(const Airport& destination) {
        Airplane::fly(destination);
    }
};

class ModelB: public Airplane {
public:
    virtual void fly(const Airport& destination) {
        Airplane::fly(destination);
    }
};

class ModelC: public Airplane {
public:
    virtual void fly(const Airport& destination);
};

void ModelC::fly(const Airport& destination) {
    // the implementation of fly is different from the base class
}

int main() {
    // ...
    return 0;
}