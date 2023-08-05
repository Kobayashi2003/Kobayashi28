#include <iostream>

using std::cout;
using std::cin;
using std::endl;

class Rational {
private:
    int _x, _y;
public:
    Rational() : _x(0), _y(1) {}
    Rational(int x, int y=1) {
        int sinal = 1;
        if (x < 0) {
            x = -x;
            sinal *= -1;
        }
        if (y < 0) {
            y = -y;
            sinal *= -1;
        }
        int min = (x < y ? x : y);
        for (int i = min; i > 1; --i) {
            if (!(x % i) && !(y % i)) { x /= i; y /= i; }
            else if (x == 1 || y == 1) { break; }
        }
        _x = x*sinal; _y = y;
    }
    Rational(const Rational & r) : _x(r._x), _y(r._y) {}
    ~Rational() = default;

    Rational operator+(const Rational & r) const {
        int x = _x*r._y + r._x*_y, y = _y * r._y;
        Rational result(x, y);
        return result;
    }

    Rational operator-(const Rational& r) const {
        int x = _x*r._y - r._x*_y, y = _y * r._y;
        Rational result(x, y);
        return result;
    }

    Rational operator*(const Rational& r) const {
        int x = _x * r._x, y = _y * r._y;
        Rational result(x, y);
        return result;
    }

    Rational operator/(const Rational& r) const {
        int x = _x * r._y, y = _y * r._x;
        Rational result(x, y);
        return result;
    }

    bool operator==(const Rational & r) const {
        return (double)_x/_y == (double)r._x/r._y;
    }

    bool operator!=(const Rational & r) const {
        return !(*this == r);
    }

    bool operator<(const Rational & r) const {
        return (double)_x/_y < (double)r._x/r._y;
    }

    bool operator>(const Rational & r) const {
        return !(*this < r || *this == r);
    }

    bool operator<=(const Rational & r) const {
        return !(*this > r);
    }

    bool operator>=(const Rational & r) const {
        return !(*this < r);
    }

    Rational operator++(int) {
        Rational tmp = *this;
        *this = *this + Rational(1);
        return tmp;
    }

    Rational & operator++() {
        *this = *this + Rational(1, 1);
        return *this;
    }

    operator double() const { return (double)_x / _y; }

    friend std::ostream& operator<<(std::ostream& os, const Rational& r) {
        // r.Print();
        os << r._x << "/" << r._y;
        return os;
    }

    void Print() const {
        cout << _x << "/" << _y << endl;
    }
};

void solve1(const Rational & r1, const Rational & r2) {
    r1.Print();
    r2.Print();
    (r1 + r2).Print();
    (r1 - r2).Print();
    (r1 * r2).Print();
    (r1 / r2).Print();
}

void solve2(const Rational & r1, const Rational & r2) {
    cout << r1 << endl << r2 << endl;
    if (r1 > r2) {
        cout << "bigger" << endl;
    } else if (r1 < r2) {
        cout << "smaller" << endl;
    } else {
        cout << "equal" << endl;
    }
    Rational tmp = r1;
    cout << ++tmp << endl;
}

void solve3(const Rational& r1, const Rational& r2, double d) {
    cout << r1 << endl << r2 << endl;
    cout << r1 + r2 << endl;
    cout << (double)r1 + d << endl;
}

int main() {
    // int x1, y1, x2, y2;
    // cin >> x1 >> y1 >> x2 >> y2;
    // Rational r1(x1, y1), r2(x2, y2);

    int x1, y1, x2;
    double d;
    cin >> x1 >> y1 >> x2 >> d;
    Rational r1(x1, y1), r2(x2);
    solve3(r1, r2, d);
    return 0;
}