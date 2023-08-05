#include <iostream>

template <auto N>
void f() {
    std::cout << N << std::endl;
}

int main() {
    f<5>();
    f<'c'>();
    // f<1.0>(); 模板参数不饿能为 double 类型
    return 0;
}