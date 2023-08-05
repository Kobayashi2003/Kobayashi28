#include <iostream>

int x = 1;

int main() {

    int y = 2;

    static int z = 3;

    int num;
    std::cin >> num;

    auto foo = [y](int num){return x*y*z*num;};

    std::cout << foo(num) << std::endl;

    return 0;
}