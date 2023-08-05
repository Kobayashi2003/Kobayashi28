// 3
// 类体外定义成员函数

#include <iostream>

class Time {
private:
    int hour, minute, second;
public:
    Time();
    void print();
};

Time::Time() {
    std::cin >> hour >> minute >> second;
}

void Time::print() {
    std::cout << hour << ":" << minute << ":" << second << std::endl;
}

int main() {
    Time time;
    time.print();
    return 0;
}
