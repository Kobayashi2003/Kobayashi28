#include <iostream>

int main() {


    auto l = [](auto x, auto y) {return x + y;};
    auto retval = l(1, 20.0);
    std::cout << retval << std::endl;

    return 0;
}