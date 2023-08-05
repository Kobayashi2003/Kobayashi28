#include <iostream>
#include <string>

class Teacher {
private:
    std::string _name;
    std::string _sex;
    int _num;
    int _age = 30;
public:
    Teacher() = default;
    Teacher(std::string name, std::string sex, int num) : _name(name), _sex(sex), _num(num) {}
    void self_introduction() {
        std::cout << "I am a teacher." << std::endl;
        std::cout << "name: " << _name << std::endl;
        std::cout << "sex: " << _sex << std::endl;
        std::cout << "num: " << _num << std::endl;
        std::cout << "age: " << _age << std::endl;
    }
};

class Student {
private:
    std::string _name = "XiaoMing";
    std::string _sex = "Male";
    int _num = 1001;
    int _age = 17;
public:
    Student() = default;
    operator Teacher() { return Teacher(_name, _sex, _num); }
    void self_introduction() {
        std::cout << "I am a student." << std::endl;
        std::cout << "name: " << _name << std::endl;
        std::cout << "sex: " << _sex << std::endl;
        std::cout << "num: " << _num << std::endl;
        std::cout << "age: " << _age << std::endl;
    }
};

int main() {
    Student s;
    s.self_introduction();
    std::cout << std::endl;
    Teacher t = s;
    t.self_introduction();
    return 0;
}