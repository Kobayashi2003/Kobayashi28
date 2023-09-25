#ifndef MYSTRING_H_
#define MYSTRING_H_
#include<iostream>
#include<cstring>
using std::ostream;
using std::istream;
using std::cin;
using std::cout;

class String {
private :
    char *str; // pointer to string
    int len; // length of string
    static int num_strings; // number of strings
    static const int CINLIM = 80; // cin input limit
public :
// constructor and other methods
    String(const char *s); // constructor
    String(); // default constructor
    String(const String &s); // copy constructor
    ~String(); // destructor
    int length() const {return len;}
// overloaded operator methods
    String & operator=(const String &);
    String & operator=(const char *);
    char & operator[](int i);
    const char & operator[](int i) const;
// overloaded operator friends
    friend bool operator<(const String &st1, const String &st2);
    friend bool operator>(const String &st1, const String &st2);
    friend bool operator==(const String &st1, const String &st2);
    friend ostream & operator<<(ostream & os, const String &st);
    friend istream & operator>>(istream & is, String &st);
// static function
    static int HowMany();
};
#endif

// initializing static class member
int String::num_strings = 0;

// static method
int String::HowMany() {
    return num_strings;
}

// class methods
String::String(const char *s) {// construct String from C string
    len = std::strlen(s); // set size
    str = new char[len + 1]; // allot storage
    std::strcpy(str, s); // initialize pointer
    num_strings++; // set object count
}

String::String() { // default constructor
    len = 0;
    str = new char[1];
    str[0] = '\0'; // default string
    num_strings++;
}

String::String(const String & st) { // copy constructor
    num_strings++; // handle static member update
    len = st.len; // copy the length
    str = new char[len + 1]; // allot space
    std::strcpy(str, st.str); // copy string to new location
}

String::~String() {// destructor
    --num_strings; // required
    delete [] str; // required
}

// overloaded operator methods
    // assign a String to a String
String & String::operator=(const String & st) {
    if(this == &st) {
        return *this;
    }
    delete [] str; // delete the old string
    len = st.len; // copy the length
    str = new char[len + 1]; // allocate new string
    std::strcpy(str, st.str); // copy string to new
    return *this;
}

    // assign a C to a String
String & String::operator=(const char * s) {
    delete [] str;
    len = std::strlen(s);
    str = new char[len + 1];
    std::strcpy(str, s);
    return *this;
}

    // read-write char access for non-const String
char & String::operator[](int i) {
    return str[i];
}

    // read-only char access for const String
const char & String::operator[](int i) const {
    return str[i];
}

// overloaded operator friends

bool operator<(const String &st1, const String &st2) {
    return (std::strcmp(st1.str, st2.str) < 0);
}

bool operator>(const String &st1, const String &st2) {
    return st2 < st1; // you don't need to write strcmp again
}

bool operator==(const String &st1, const String &st2) {
    return (std::strcmp(st1.str, st2.str) == 0);
}

    // simple String output
ostream & operator<<(ostream & os, const String &st) {
    os << st.str;
    return os;
}

    // quick and dirty input
istream & operator>>(istream & is, String &st) {
    char temp[String::CINLIM];
    is.get(temp, String::CINLIM);
    if(is) {
        st = temp;
    }
    while(is && is.get() != '\n') { // throw away extra characters
        continue;
    }
    return is;
}