#include <iostream>

class A {
private:
    int a;
    decltype(a) b;
public:
    template<typename T1, typename T2>
    static auto add(T1 x, T2 y) -> decltype(x + y) {
        return x + y;
    } 
};

int main() {
    std::cout << A::add(1, 2.3) << std::endl;
    return 0;    
}