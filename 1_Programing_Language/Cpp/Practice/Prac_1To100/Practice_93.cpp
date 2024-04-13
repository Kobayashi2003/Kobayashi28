#include <iostream>

class Date {

public:

    Date() : month(0), day(0), year(0) {}
    Date(int m, int d, int y) : month(m), day(d), year(y) {}
    Date(const Date& date) : month(date.month), day(date.day), year(date.year) {}

    int operator-(const Date& date) {

        int days = 0;
        bool isnegative = false;
        Date big_date;
        Date small_date;
        if (year > date.year || (year == date.year && month > date.month) || (year == date.year && month == date.month && day > date.day)) {
            big_date = *this;
            small_date = date;
        } else {
            big_date = date;
            small_date = *this;
            isnegative = true;            
        }


        // count days from small_date to big_date
        while (small_date.year != big_date.year || small_date.month != big_date.month || small_date.day != big_date.day) {
            days += 1;
            small_date.day += 1;
            if (small_date.month == 1 || small_date.month == 3 || small_date.month == 5 || small_date.month == 7 || small_date.month == 8 || small_date.month == 10 || small_date.month == 12) {
                if (small_date.day > 31) {
                    small_date.day = 1;
                    small_date.month += 1;
                }
            } else if (small_date.month == 4 || small_date.month == 6 || small_date.month == 9 || small_date.month == 11) {
                if (small_date.day > 30) {
                    small_date.day = 1;
                    small_date.month += 1;
                }
            } else if (small_date.month == 2) {
                if ((small_date.year % 4 == 0 && small_date.year % 100 != 0) || small_date.year % 400 == 0) {
                    if (small_date.day > 29) {
                        small_date.day = 1;
                        small_date.month += 1;
                    }
                } else {
                    if (small_date.day > 28) {
                        small_date.day = 1;
                        small_date.month += 1;
                    }
                }
            }
            if (small_date.month > 12) {
                small_date.month = 1;
                small_date.year += 1;
            }
        }

        if (isnegative) {
            days = -days;
        }
        return days;
    }

private:

    int month, day, year;

};


int main() {

    Date date1(1, 1, 2022);
    Date date2(12, 31, 2021);
    std::cout << date1 - date2 << std::endl;

    return 0;
}