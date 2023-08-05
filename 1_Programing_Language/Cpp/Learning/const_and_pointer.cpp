#include <iostream>

// 常量指针与指针常量的区别
// 常量指针：指针指向的值不能被修改
// 指针常量：指针本身不能被修改

int main() {
    // 常量指针的例子
    int a = 10;
    int b = 20;
    const int *p = &a;  // 常量指针，指针指向的值不能被修改
    std::cout << "*p = " << *p << std::endl;
    // *p = 100;  // error
    p = &b; // 但是指针本身可以被修改
    std::cout << "*p = " << *p << std::endl;

    // 指针常量的例子
    int c = 100;
    int d = 200;
    int * const p2 = &c;  // 指针常量，指针本身不能被修改
    std::cout << "*p2 = " << *p2 << std::endl;
    *p2 = 1000; // 指针指向的值可以被修改
    std::cout << "*p2 = " << *p2 << std::endl;
    // p2 = &d;  // error

    return 0;

}