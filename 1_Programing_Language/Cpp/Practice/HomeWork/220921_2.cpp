#include <iostream>
// #include <iomanip>

using namespace std ;

class Time {
public:
    int _Hour = 0;
    int _Minute = 0;
    int _Second = 0;
public:
    Time() {}
    void setTime() {
        int Hour, Minute, Seconds;
        cin >> Hour >> Minute >> Seconds;
        _Hour = Hour; _Minute = Minute; _Second = Seconds;
    }

    void setTime(const std::string& str_time_) {

        int ord = 0, tmp = 0;
        for (const auto& i : str_time_) {

            if (i >= '0' && i <= '9') {
                tmp = tmp*10 + i - '0';
            } else {
                ord += 1;
                tmp = 0;
            }

            if (ord == 0) {
                _Hour = tmp;
            } else if (ord == 1) {
                _Minute = tmp;
            } else {
                _Second = tmp;
            }

        }
    }

    void print() {
        // cout << setw(2) << setfill(0) << _Hour << ":" << setw(2) << setfill(0) << _Minute << ":" << setw(2) << setfill(0) << _Second << endl;
        if (_Hour < 10) {
            cout << 0 << _Hour;
        } else {
            cout << _Hour;
        }
        cout << ":";
        if (_Minute < 10) {
            cout << 0 << _Minute;
        } else {
            cout << _Minute;
        }
        cout << ":";
        if (_Second < 10) {
            cout << 0 << _Second;
        } else {
            cout << _Second;
        }
        cout << endl;
    }
};

int main() {
    Time t1;
    t1.setTime();

    Time t2;
    std::string str_time;
    std::cin >> str_time;
    t2.setTime(str_time);

    t1.print();
    t2.print();
    return 0;
}