#include <iostream>
#include <stdexcept>

using namespace std;

// Rational.h
class Rational {
public:
    /*constructor*/
    Rational() = default;
    Rational(int x, int y);

    /*overload operator*/
    Rational operator+(const Rational & r) const;
    Rational operator-(const Rational & r) const;
    Rational operator*(const Rational & r) const;
    Rational operator/(const Rational & r) const;
    operator double() const; // convert to double

    /*overload stream extraction operator*/
    friend ostream & operator<<(ostream & os, const Rational & r);


private: // private member
    int _x = 0, _y = 1; // _x is numerator, _y is denominator, and _x/_y is the rational number.

private: // private function
    void simplify(); // simplify the rational number to the simplest form.
};

// Rational.cpp
// #include "Rational.h"
Rational::Rational(int x, int y) {
    if (y == 0) {
        throw "error";
    }
    _x = x; _y = y;
    simplify();
}

Rational Rational::operator+(const Rational & r) const {
    Rational temp;
    temp._x = _x * r._y + _y * r._x;
    temp._y = _y * r._y;
    temp.simplify();
    return temp;
}

Rational Rational::operator-(const Rational & r) const {
    Rational temp;
    temp._x = _x * r._y - _y * r._x;
    temp._y = _y * r._y;
    temp.simplify();
    return temp;
}

Rational Rational::operator*(const Rational & r) const {
    Rational temp;
    temp._x = _x * r._x;
    temp._y = _y * r._y;
    temp.simplify();
    return temp;
}

Rational Rational::operator/(const Rational & r) const {
    if (r._x == 0) {
        throw "error";
    }
    Rational temp;
    temp._x = _x * r._y;
    temp._y = _y * r._x;
    temp.simplify();
    return temp;
}

Rational::operator double() const {
    return (double)_x / _y;
}

ostream & operator<<(ostream & os, const Rational & r) {
    os << r._x << "/" << r._y;
    return os;
}

void Rational::simplify() {
    int a = _x, b = _y;
    if (a < 0) {
        a = -a;
    }
    while (a != 0) {
        int temp = a;
        a = b % a;
        b = temp;
    }
    _x /= b; _y /= b;
}

// main.cpp
// #include "Rational.h"
int main() {
    int x1, y1, x2, y2;
    cin >> x1 >> y1 >> x2 >> y2;
    try {
        Rational r1(x1, y1), r2(x2, y2);
        cout << r1 + r2 << endl;
    } catch (const char * e) {
        cerr << e << endl;
    }

    return 0;
}