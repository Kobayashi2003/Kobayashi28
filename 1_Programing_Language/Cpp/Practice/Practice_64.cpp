#include <iostream>

using LLI = long long int;

LLI qpow(int x, int y) {
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

int main() {
    int x, y;
    std::cin >> x >> y;
    std::cout << qpow(x, y) << std::endl;
    return 0;
}