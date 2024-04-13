#include<iostream>
#include<string>

using namespace std;

class People {
private :
    string _name;
    int _age;
public :
    People(string name = "xiaoming", int age = 17) {
        _name = name; _age = age;
    }
    ~People() {};
    friend ostream & operator<<(ostream & os, const People & p);
};

ostream & operator<<(ostream & os, const People & p) {
    os << "name: " << p._name << endl << "age: " << p._age << endl;
    return os;
}

int main() {
    People xiaoming, xiaowang("xiaowang");
    cout << xiaoming << xiaowang;
    return 0;
}