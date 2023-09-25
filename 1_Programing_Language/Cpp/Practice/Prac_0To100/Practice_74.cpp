#include <iostream>
#include <sstream>
#include <string>   

using namespace std;

void test1() {
    string s = "ABCD";
    stringstream ss(s);
    char ch;
    while (ss>>ch) {
        cout << ch << " ";
    }
}

void test2() {
    string s = "hello world";
    stringstream ss(s);
    string str;
    while (ss>>str) {
        cout << str << "-";
    }
}

void test3() {
    stringstream stream;
    int a, b;

    stream << "80";
    stream >> a;
    cout << "Size of stream = " << stream.str().length() << endl;

    stream.clear(); // clear flags
    stream.str(""); // clear buffer contents
    cout << "Size of stream = " << stream.str().length() << endl;

    stream << "90";
    stream >> b;
    cout << "Size of stream = " << stream.str().length() << endl;

    cout << a << " " << b << endl;   
}

int main() {
    test3(); 
    return 0;
}