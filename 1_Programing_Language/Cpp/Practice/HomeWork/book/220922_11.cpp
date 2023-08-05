// 输入一个字符串，把期中的字符按逆序输出，要求使用string方法

#include <iostream>
#include <string>

int main() {
    std::string str;
    std::getline(std::cin, str);
    for (auto prep = str.rbegin(); prep != str.rend(); ++prep) { // 逆向迭代
        std::cout << *prep;
    }
    return 0;
}