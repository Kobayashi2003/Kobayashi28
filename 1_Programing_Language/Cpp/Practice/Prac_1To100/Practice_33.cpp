#include<iostream>
#include<string>

using namespace std;

class People {
private :
    string _name;
    int _age;
public :
    People(string name = "xiaoming", int age = 18) {
        _name = name; _age = age;
    }
    ~People() {}
    friend void operator<<(ostream & os, const People & p);
};

void operator<<(ostream & os, const People & p) {
    os << "name: " << p._name << endl << "age: " << p._age << endl;
}

int main() {
    People p;
    cout << p;
    return 0;
}