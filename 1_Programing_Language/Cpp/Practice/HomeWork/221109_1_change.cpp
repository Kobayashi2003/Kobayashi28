/* Sample Input
int
1 1
1 1
1
*/

/* Sample Output
1+2i
0
1-2i
*/


#include <iostream>

template<typename eT>
class Complex {
public:
    eT _real;
    eT _imag;

    /* constructor and destructor */
    Complex() : _real(0), _imag(0) {}
    Complex(eT real, eT imag) : _real(real), _imag(imag) {}
    ~Complex() = default;

    /* operator overloading */

    // object + object
    Complex operator+(const Complex &other) const { return Complex(_real + other._real, _imag + other._imag); }
    Complex operator-(const Complex &other) const { return Complex(_real - other._real, _imag - other._imag); }
    Complex operator*(const Complex &other) const { return Complex(_real * other._real - _imag * other._imag, _real * other._imag + _imag * other._real); }

    // object + eT
    Complex operator+(const eT &other) const { return Complex(_real + other, _imag); }
    Complex operator-(const eT &other) const { return Complex(_real - other, _imag); }
    Complex operator*(const eT &other) const { return Complex(_real * other, _imag * other); }

    // eT + object (friend function)
    friend Complex operator+(const eT &data, const Complex &other) { return Complex(data + other._real, other._imag); }

    friend Complex operator-(const eT &data, const Complex &other) { return Complex(data - other._real, -other._imag); }

    friend Complex operator*(const eT &data, const Complex &other) { return Complex(data * other._real, data * other._imag); }

    void print();
};

template<typename eT>
void Complex<eT>::print() {
    std::cout << _real;
    if (_imag > 0) {
        std::cout << "+";
    }
    if (_imag != 0) {
        std::cout << _imag << "i";
    }
    std::cout << std::endl;
}

int main() {
	std::string data_type;
	std::cin >> data_type;
	if (data_type == "int") {
		Complex<int> a, b;
		std::cin >> a._real >> a._imag;
		std::cin >> b._real >> b._imag;
		int f;
		std::cin >> f;
		Complex<int> c = a + b - f; c.print();
		Complex<int> d = a - f * b; d.print();
		Complex<int> e = f - a * b; e.print();
	}
	else if (data_type == "float") {
		Complex<float> a, b;
		std::cin >> a._real >> a._imag;
		std::cin >> b._real >> b._imag;
		float f;
		std::cin >> f;
		Complex<float> c = a + b - f; c.print();
		Complex<float> d = a - f * b; d.print();
		Complex<float> e = f - a * b; e.print();
	}
	else if (data_type == "double") {
		Complex<double> a, b;
		std::cin >> a._real >> a._imag;
		std::cin >> b._real >> b._imag;
		double f;
		std::cin >> f;
		Complex<double> c = a + b - f; c.print();
		Complex<double> d = a - f * b; d.print();
		Complex<double> e = f - a * b; e.print();
	}
	return 0;
}