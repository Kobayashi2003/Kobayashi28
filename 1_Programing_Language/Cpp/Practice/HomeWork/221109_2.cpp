#include <iostream>


class String {
public:
    char* _p;             //以'\0'结尾
    static int _capacity; //最大容量
public:
    String(); //要求在无传参构造函数里输入字符串_p
    String(char* src);
    String(const String& src);
    ~String();
    //需要补充“+”和“>”的运算符重载

    String operator+(const String& other) const;
    bool operator>(const String& other) const;

    void print();
};

int String::_capacity = 100;

String::String() {
    _p = new char[_capacity];
    std::cin >> _p;
}

String::String(char* src) {
    _p = new char[_capacity];
    int i = 0;
    while (src[i] != '\0') {
        _p[i] = src[i];
        i++;
    }
    _p[i] = '\0';
}

String::String(const String& src) {
    _p = new char[_capacity];
    int i = 0;
    while (src._p[i] != '\0') {
        _p[i] = src._p[i];
        i++;
    }
    _p[i] = '\0';
}

String::~String() {
    delete[] _p;
}

String String::operator+(const String& other) const {
    String result;
    int i = 0;
    while (_p[i] != '\0') {
        result._p[i] = _p[i];
        i++;
    }
    int j = 0;
    while (other._p[j] != '\0') {
        result._p[i] = other._p[j];
        i++;
        j++;
    }
    result._p[i] = '\0';
    return result;
}

bool String::operator>(const String& other) const {
    int i = 0;
    while (_p[i] != '\0' && other._p[i] != '\0') {
        if (_p[i] > other._p[i]) {
            return true;
        }
        else if (_p[i] < other._p[i]) {
            return false;
        }
        i++;
    }
    if (_p[i] == '\0' && other._p[i] != '\0') {
        return false;
    }
    else {
        return true;
    }
}

void String::print() {
    std::cout << _p << std::endl;
}

int main() {
	String str_a;
	String str_b;
	//比较大小
	std::cout << (str_a > str_b) << std::endl;
	//字符串合并
	String str_c = str_a + str_b;
	str_c.print();
	return 0;
}