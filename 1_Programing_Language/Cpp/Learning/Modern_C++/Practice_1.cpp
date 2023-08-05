#include <iostream>

namespace A::B::inline C {
    int function() {return 20;}
}

int main() {
    std::cout << A::B::function() << std::endl;
    return 0;
}