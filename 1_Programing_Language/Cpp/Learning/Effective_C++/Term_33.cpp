// Avoid hiding inherited names
// 避免遮掩继承而来的名字

// derved classes 内的名称会遮掩 base classes 内的名称
// 为了使 base classes 内的名称在 derived classes 内可见，可使用 using 声明式或转交函数 （forwarding functions）

#include <iostream>

class Base {
private:
    int x;
public:
    virtual void mf1 () = 0;
    virtual void mf1 (int) {
        std::cout << "Base::mf1(int)" << std::endl;
    }
    virtual void mf2 () {
        std::cout << "Base::mf2()" << std::endl;    
    }
    void mf3 () {
        std::cout << "Base::mf3()" << std::endl;
    }
    void mf3 (double) {
        std::cout << "Base::mf3(double)" << std::endl;
    }
};

void Base::mf1() {
    std::cout << "Base::mf1()" << std::endl;
}

class Derived : public Base {
public:
    using Base::mf1; // make mf1() visible
    using Base::mf3; // make mf3() visible

    virtual void mf1 () { // forward function
        Base::mf1();
    }

    virtual void mf1 (int) {
        std::cout << "Derived::mf1(int)" << std::endl;
    }
    void mf3 () {
        std::cout << "Derived::mf3()" << std::endl;
    }
    void mf4 () {
        std::cout << "Derived::mf4()" << std::endl;
    }
};

int main() {
    Derived d;
    int x = 0; 
    d.mf1(); // Derived::mf1()
    d.mf1(x); // Base::mf1(int)
    d.mf2(); // Base::mf2()
    d.mf3(); // Derived::mf3()
    d.mf3(x); // Base::mf3(double)  
    return 0;
}