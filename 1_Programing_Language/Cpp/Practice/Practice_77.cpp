#include <iostream>
#include <string>

std::string operator "" _s(const char* str, size_t len) {
    return std::string(str, len);
}


int main() {
    std::string str = "Hello World!"_s;
    std::cout << str << std::endl;
    return 0;
}