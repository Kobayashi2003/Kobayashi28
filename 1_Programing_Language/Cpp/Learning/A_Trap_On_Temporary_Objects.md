# C++ —— 非常量引用不能指向临时对象

首先来看一个例子

```cpp
#include <iostream>
#include <typeinfo>

class A {
public: 
    int _data;

    /* construction and distruction */
    A() : _data(0) {}
    A(int data) : _data(data) {}

    /* overloaded operator fucntion */
    A operator+(const A &a) const;
    
    friend std::ostream & operator<<(std::ostream &out, A &a);
};

A A::operator+(const A &a) const {
    return A(_data + a._data);
}

std::ostream &operator<<(std::ostream &out, A &a) {
    std::cout << a._data;
    return out;
}

int main() {
    A a1, a2;
    std::cout << typeid(a1+a2).name() << std::endl; // 1A
    std::cout << a1 + a2;
    // 在本例中此处将会报错
    // 错误信息：	
    // "message": "no match for 'operator<<' (operand types are 'std::ostream' {aka 'std::basic_ostream<char>'} and 'A')",
    // "message": "cannot bind non-const lvalue reference of type 'A&' to an rvalue of type 'A'",
    return 0;
}
```

例一中的报错分析：

实际上，在 `main` 函数中的 `a1+a2` 返回的是一个 A类的临时对象，然而 `<<` 操作函数的参数却是 `A &a`。

以C++的语义来说，如果一个程序员只想传递参数给函数，而不希望函数修改传入的参数时，那么，或者使用值传递，或者采用常量型引用。考虑到大对象复制时产生的开销，我们一般采用常量型引用 `const &` 的方式进行函数间的对象的传递。如果函数的参数时某个类型的一个非常量的引用，那就相当于告诉编译器，程序员希望得到函数对参数修改结果。

而临时变量是由编译器产生的，程序员无法得知由编译器生成的临时变量的名字，程序员也即无法通过对应的变量名来访问该临时变量.

由此有一个c++编译器的一个关于语义的限制。如一个参数是以非const引用传入，c++编译器就有理由认为程序员会在函数中修改这个值，并且这个被修改的引用在函数返回后要发挥作用。如果你一个临时变量当作非const引用参数传进来，由于临时变量的特殊性，程序员并不能操作临时变量，而且临时变量随时可能被释放掉，所以，一般说来，修改一个临时变量是毫无意义的，据此，c++编译器加入了**临时变量不能作为非const引用**的这个语义限制，意在限制这个非常规用法的潜在错误。


最终，我们可以得到该问题的解决方案：

- 第一种就是将 `operator<<` 重载函数参量中的**非常量引用**改为**值传递**的形式
```cpp
friend std::ostream & operator<<(std::ostream & out, A a) {
    std::cout << a._data;
    return out;
}
```

- 第二种就是将 `operator<<` 重载函数参量中的**非常量引用**改为**常量引用**的形式
```cpp
friend std::ostream & operator<<(std::ostream & out, const A &a) {
    std::cout << a._data；
    return out;
}
```

- 第三种是通过修改成员函数 `operator+`，使其在函数执行的最后返回一个**实际的对象引用**（注意：不能够将函数中产生的临时对象的引用作为参数返回原函数），从而避免临时对象的产生
```cpp
A & A::operator+(const &other) const {
    auto new_a = A(_data + other._data);
    return *new_a;
}
```

当然，考虑到安全、开销以及书写的便利性，个人推荐使用第二种方法

> END

[参考文章1](https://www.cnblogs.com/BensonLaur/p/5234555.html)
[参考文章2](https://www.cnblogs.com/dongzhiquan/p/3222083.html)