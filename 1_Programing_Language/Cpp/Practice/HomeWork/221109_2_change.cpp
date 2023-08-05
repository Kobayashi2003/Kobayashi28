#include <iostream>

class String {

public:
    /* Static Data */
    constexpr static const int _capacity = 100; // the maximum capacity

    /* Public Data */
    char* _p; // end with '\0'
    
    /* constructor and distructor */
    String() {// input string _p in the constructor without parameters
        _p = new char[_capacity]; std::cin >> _p;
    }
    String(const char* src) { // copy constructor (char*)
        _p = new char[_capacity];
        int i = 0;
        while (src[i] != '\0') { _p[i] = src[i]; i+=1; }
        _p[i] = '\0';
    }
    String(const String& src) { // copy constructor (String&)
        _p = new char[_capacity];
        int i = 0;
        while (src._p[i] != '\0') { _p[i] = src._p[i]; i+=1; }
        _p[i] = '\0';
    }
    ~String() { delete[] _p; }

    /* operator overload */
    // Sring --- String //
    String operator+(const String& other) const;
    bool operator==(const String& other) const;
    bool operator>(const String& other) const;
    bool operator<(const String& other) const;

    void print();
};

String String::operator+(const String& other) const {
    String result("");
    int i = 0;
    while (_p[i] != '\0') { result._p[i] = _p[i]; i+=1; }
    int j = 0;
    while (other._p[j] != '\0') { result._p[i++] = other._p[j++]; }
    result._p[i] = '\0';
    return result;
}

bool String::operator==(const String& other) const {
    int i = 0;
    while (_p[i] != '\0' && other._p[i] != '\0') {
        if (_p[i] != other._p[i]) { return false; }
        i+=1;
    }
    return _p[i] == other._p[i];
}

bool String::operator>(const String& other) const {
    int i = 0;
    while (_p[i] != '\0' || other._p[i] != '\0') {
        if (_p[i] > other._p[i]) { return true; }
        else if (_p[i] < other._p[i]) { return false; }
        i+=1;
    }
    return false;
}

bool String::operator<(const String& other) const {
    return !(*this > other) && !(*this == other);
}

void String::print() { std::cout << _p << std::endl; }

int main() {
	String str_a;
	String str_b;
	std::cout << (str_a > str_b) << std::endl;
	String str_c = str_a + str_b;
	str_c.print();
	return 0;
}