#include <iostream>

using namespace std;

class Date;

class Time {
private:
    int hour;
    int minute;
    int second;
public:
    Time(int h, int m, int s) : hour(h), minute(m), second(s) {}
    void display(Date &d);
};

class Date {
private:
    int month;
    int day;
    int year;
public:
    Date(int m, int d, int y) : month(m), day(d), year(y) {}
    friend void Time::display(Date &d);
};

void Time::display(Date &d) {
    cout << d.month << "/" << d.day << "/" << d.year << endl;
    cout << hour << ":" << minute << ":" << second << endl;
}

int main() {

    Time t1(10, 13, 56);
    Date d1(12, 25, 2004);
    t1.display(d1);

    return 0;
}