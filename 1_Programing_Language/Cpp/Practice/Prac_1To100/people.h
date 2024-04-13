#ifndef PEOPLE_H_
#define PEOPLE_H_
#include<iostream>
#include<string>
class People {
private :
    std::string _name;
    mutable int _age;
public :
    People(std::string name = "xiao ming", int age = 18) {
        _name = name; _age = age;
        std::cout << "construtor work" << std::endl;
    }
    People(const People & other) {
        _name = other._name; _age = other._age;
        std::cout << "copy construtor work" << std::endl;
    }
    ~People() {
        std::cout << "destructor work" << std::endl;
    }
    friend std::ostream & operator<<(std::ostream & os, const People & p) {
        os << "name: " << p._name << std::endl << "age: " << p._age << std::endl;
        return os;
    }
    friend People & operator+(People & p, int num) {
        p._age += num;
        return p;
    }
};
#endif