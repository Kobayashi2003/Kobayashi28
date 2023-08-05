// 2
// 将数据成员改为私有
// 将输入和输出的功能改为由成员函数实现
// 再类体内定义成员函数

#include <iostream>

class Time {
private:
    int hour, minute, second;
public:
    Time() {
        std::cin >> hour >> minute >> second;
    }

    void print() {
        std::cout << hour << ":" << minute << ":" << second << std::endl;
    }
};

int main() {
    Time time;
    time.print();
    return 0;
}
