// constexpr 常量表达式

// 将运行时的计算提前到编译时来做性能优化

#include <iostream>

using LLI = long long int;

constexpr LLI qpow(int x, int y) {
    LLI tmp_x = x, result = 1;
    while (y > 0) {
        if (y & 1) { // 若 y 为奇数
            result *= tmp_x;
        }
        y >>= 1;
        tmp_x = tmp_x * tmp_x;
    }
    return result;
}

// 除此之外，C++17还将constexpr函数引入到if语句中，允许在代码中声明常量表达式的判断条件
    
template<typename T>
auto print_type_info(const T& t) {
    if constexpr (std::is_integral<T>::value) {
        std::cout << "Integral type" << std::endl;
        return t + 1;
    } else {
        std::cout << "Not integral type" << std::endl;
        return t + 0.001;
    }
}

int main() {

    int arr[ qpow(2, 5) ] = {}; 

    std::cout << sizeof(arr)/sizeof(int) << std::endl;

    std::cout << print_type_info(5) << std::endl;
    std::cout << print_type_info(3.14) << std::endl;


    return 0;
}