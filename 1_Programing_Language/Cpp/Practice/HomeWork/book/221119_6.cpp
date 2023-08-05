#include <iostream>

class Complex {
private:
    double real, imag;
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    Complex operator+(double num) {
        return Complex(real + num, imag);
    }
    friend Complex operator+(double num, Complex& c) {
        return Complex(c.real + num, c.imag);
    }

    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        if (c.real) {
            os << c.real;
            if (c.imag) {
                os << (c.imag > 0 ? "+" : "") << c.imag << "i";
            }
        } else {
            os << c.imag << "i";
        }
        return os;
    }

    operator double() const { return real; }
};

int main() {
    Complex c(2.3, 4.5);
    double d = c + 0.5;
    std::cout << d << std::endl;
    std::cout << Complex(d) << std::endl;
    return 0;
}