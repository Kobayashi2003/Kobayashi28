#include <iostream>
#include <string>
#include <limits>
#include <iomanip>

using ULL = unsigned long long int;

/* Class */

class Time {
private:
    enum {year=0, month=1, day=2, hour=3, minute=4};
    ULL *time;

public:

    Time(std::string input);
    ~Time();

    bool check() const;
    void show() const;

    static bool compare(const Time & a, const Time & b);
};

/* Class End */

/* Time Class Function Definition */
Time::Time(std::string input) {
    time = new ULL[5] {0};
    for (int flg=0, i=0; i < (int)input.length(); ++i) {
        if (input[i] >= '0' && input[i] <= '9') {
            time[flg] = time[flg]*10 + input[i] - '0';
        }
        else {
            flg += 1;
        }
    }
}

Time::~Time() { delete [] time; }

bool Time::compare(const Time& t1, const Time& t2) {
    for (int i = 0; i < 5; i += 1) {
        if (t1.time[i] < t2.time[i]) {
            return true;
        } else if (t1.time[i] == t2.time[i]) {
            continue;
        }
        break;
    }
    return false;
}

bool Time::check() const {
    ULL day_standard[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // check the year
    if (time[year] < 0) {
        return false;
    }

    if ((time[year] % 4 == 0 && time[year] % 100 != 0) ||
        (time[year] % 400 == 0))
    {
        day_standard[2] += 1;
    }

    // cheak the month
    if (time[month] < 0 || time[month] > 12) {
        return false;
    } else { // then check the days in the month
        if (time[day] < 0 || time[day] > day_standard[time[month]]) {
            return false;
        }
    }

    // finally check the hour and minute
    if (time[hour] < 0 || time[hour] > 24) {
        return false;
    }
    if (time[minute] < 0 || time[minute] > 60) {
        return false;
    }

    return true;
}

void Time::show() const {
    std::cout << time[year] << "/"
              << time[month] << "/"
              << time[day] << " "
              << std::setw(2) << std::setfill('0') << time[hour] << ":"
              << std::setw(2) << std::setfill('0') << time[minute]
              << std::endl;
}
/* Time Class Function End */


int main() {
    std::string input = "";
    std::getline(std::cin, input);
    Time t1(input);

    //std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::getline(std::cin, input);
    Time t2(input);


    if (!t1.check() || !t2.check()) {
        std::cout << "time invalid." << std::endl;
        return 0;
    }

    t1.show();
    t2.show();


    std::cout << Time::compare(t1, t2) << std::endl;

    return 0;
}