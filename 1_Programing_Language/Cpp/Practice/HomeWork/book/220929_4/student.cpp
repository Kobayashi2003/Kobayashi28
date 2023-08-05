#include <iostream>
#include "student.h"

void Student::set_value(int num, std::string name, char sex) {
    _num = num;
    _name = name;
    _sex = sex;
}

void Student::display() const {
    std::cout << "num: " << _num << std::endl;
    std::cout << "name: " << _name << std::endl;
    std::cout << "sex: " << _sex << std::endl;
}
