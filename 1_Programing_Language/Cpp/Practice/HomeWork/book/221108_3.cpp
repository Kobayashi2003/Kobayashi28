#include <iostream>

class Date {
private:
    int month, day, year;

public:
    Date(int=1, int=1, int=2005);
    void display();
};

Date::Date(int m, int d, int y) : month(m), day(d), year(y) {}

void Date::display() {
    std::cout << month << "/" << day << "/" << year << std::endl;
}

int main() {
    Date d1(10, 13, 2005);
    Date d2(12, 30);
    Date d3(10);
    Date d4;
    d1.display();
    d2.display();
    d3.display();
    d4.display();
    return 0;
}