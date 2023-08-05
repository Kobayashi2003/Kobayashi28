#include <iostream>
#include <string>
#include <algorithm>


int main () {
    std::string str = "";
    // str += std::to_string(12);
    // std::cout << str << std::endl;
    int num; std::cin >> num;
    if (num) {
        while (num) {
            str += std::to_string(num % 10);
            num /= 10;
        }
    } else {
        str += '0';
    }
    std::reverse(str.begin(), str.end());
    std::cout << str << std::endl;
    return 0;
}