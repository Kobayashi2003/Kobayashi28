#include <iostream>
using namespace std;

class Time {
private:
    int hour;
    int minute;
    int second;
public:
    Time(int h, int m, int s) : hour(h), minute(m), second(s) {}
    friend void display(Time &t);
};

class Date {
private:
    int month;
    int day;
    int year;
public:
    Date(int m, int d, int y) : month(m), day(d), year(y) {}
    friend void display(Date &d);
};

void display(Time &t) {
    cout << t.hour << ":" << t.minute << ":" << t.second << endl;
}

void display(Date &d) {
    cout << d.month << "/" << d.day << "/" << d.year << endl;
}



int main() {

    Time t1(10, 13, 56);
    Date d1(12, 25, 2004);
    
    display(t1);
    display(d1);

    return 0;
}