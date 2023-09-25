#ifndef MYHEAD_H_
#define MYHEAD_H_
#include<iostream>
#include<string>

class People {
private :
    std::string _name;
    int _age;
public :
    People(std::string name = "xiao ming", int age = 18) {
        _name = name; age = age;
        std::cout << "construtor work" << std::endl;
    }
    ~People() {
        std::cout << "destructor work" << std::endl;
    }
    void show() {
        std::cout << "name: " << _name << std::endl << "age: " << _age << std::endl;
    }
};
#endif