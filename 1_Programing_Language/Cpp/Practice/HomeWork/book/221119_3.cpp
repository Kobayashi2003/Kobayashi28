#include <iostream>

class Complex {
private:
    double _real;
    double _imag;
public:
    Complex() : _real(0), _imag(0) {}
    Complex(double real, double imag) : _real(real), _imag(imag) {}
    ~Complex() = default;
    // object + object
    Complex operator+(const Complex &other) const { return Complex(_real + other._real, _imag + other._imag); }
    // object + double
    Complex operator+(double other) const { return Complex(_real + other, _imag); }
    // double + object
    friend Complex operator+(double other, const Complex &obj) { return Complex(other + obj._real, obj._imag); }
    friend std::istream &operator>>(std::istream &is, Complex &obj) {
        is >> obj._real >> obj._imag;
        return is;
    }
    friend std::ostream &operator<<(std::ostream &os, const Complex &obj) {
        os << obj._real;
        if (obj._imag > 0) {
            os << "+";
        }
        if (obj._imag != 0) {
            os << obj._imag << "i";
        }
        return os;
    }
};

int main() {
    Complex c1(1, 2);
    Complex c2(1, -3);

    std::cout << c1 << std::endl;
    std::cout << c2 << std::endl;
    std::cout << c1 + c2 << std::endl;
    std::cout << c1 + 1 << std::endl;
    std::cout << 1 + c2 << std::endl;

    return 0;
}