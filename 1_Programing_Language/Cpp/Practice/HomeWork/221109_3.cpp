#include <iostream>

template<typename eT>
class Vector {
public:
    eT* _list;
    int _N;
public:
    Vector();
    Vector(int N);
    Vector(const Vector& src);
    ~Vector();
    void set(int index, eT src);
    //补全运算符重载函数
    Vector operator+(const Vector& other) const;
    Vector operator-(const Vector& other) const;
    Vector operator*(const Vector& other) const;
    Vector operator+(const eT& other) const;
    Vector operator-(const eT& other) const;
    Vector operator*(const eT& other) const;

    // eT data + Vector
    friend Vector operator+(const eT &data, const Vector &other) {
        Vector result(other._N);
        for (int i = 0; i < other._N; i++) {
            result._list[i] = data + other._list[i];
        }
        return result;
    }

    // eT data - Vector
    friend Vector operator-(const eT &data, const Vector &other) {
        Vector result(other._N);
        for (int i = 0; i < other._N; i++) {
            result._list[i] = data - other._list[i];
        }
        return result;
    }

    // eT data * Vector
    friend Vector operator*(const eT &data, const Vector &other) {
        Vector result(other._N);
        for (int i = 0; i < other._N; i++) {
            result._list[i] = data * other._list[i];
        }
        return result;
    }

    void print();
};

template<typename eT>
Vector<eT>::Vector() : _N(0) {
    _list = new eT[_N];
}

template<typename eT>
Vector<eT>::Vector(int N) : _N(N) {
    _list = new eT[_N];
}

template<typename eT>
Vector<eT>::Vector(const Vector &src) : _N(src._N) {
    _list = new eT[_N];
    for (int i = 0; i < _N; i++) {
        _list[i] = src._list[i];
    }
}

template<typename eT>
Vector<eT>::~Vector() {
    delete[] _list;
}

template<typename eT>
void Vector<eT>::set(int index, eT src) {
    _list[index] = src;
}

template<typename eT>
void Vector<eT>::print() {
    std::cout << "{";
    for (int i = 0; i < _N; i++) {
        std::cout << _list[i];
        if (i != _N - 1) {
            std::cout << ",";
        }
    }
    std::cout << "}" << std::endl;
}

template<typename eT>
Vector<eT> Vector<eT>::operator+(const Vector &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] + other._list[i];
    }
    return result;
}

template<typename eT>
Vector<eT> Vector<eT>::operator-(const Vector &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] - other._list[i];
    }
    return result;
}

template<typename eT>
Vector<eT> Vector<eT>::operator*(const Vector &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] * other._list[i];
    }
    return result;
}

template<typename eT>
Vector<eT> Vector<eT>::operator+(const eT &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] + other;
    }
    return result;
}

template<typename eT>
Vector<eT> Vector<eT>::operator-(const eT &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] - other;
    }
    return result;
}

template<typename eT>
Vector<eT> Vector<eT>::operator*(const eT &other) const {
    Vector<eT> result(_N);
    for (int i = 0; i < _N; i++) {
        result._list[i] = _list[i] * other;
    }
    return result;
}



int main() {
	std::string data_type;
	std::cin >> data_type;
	if (data_type == "int") {
		int N, buffer;
		std::cin >> N;
		Vector<int> a(N);
		Vector<int> b(N);
		for (int i = 0; i < N; i++) {//输入第一个数组
			std::cin >> buffer;
			a.set(i, buffer);
		}
		for (int i = 0; i < N; i++) {//输入第二个数组
			std::cin >> buffer;
			b.set(i, buffer);
		}
		Vector<int> c = a * 5 + a * b + 4 + 3 * (b - a) + (2 - a) * 1 - 0;
		c.print();
	}
	else if (data_type == "double") {
		int N;
		double buffer;
		std::cin >> N;
		Vector<double> a(N);
		Vector<double> b(N);
		for (int i = 0; i < N; i++) {//输入第一个数组
			std::cin >> buffer;
			a.set(i, buffer);
		}
		for (int i = 0; i < N; i++) {//输入第二个数组
			std::cin >> buffer;
			b.set(i, buffer);
		}
		Vector<double> c = a * 5 + a * b + 4 + 3 * (b - a) + (2 - a) * 1 - 0;
		c.print();
	}
	return 0;
}