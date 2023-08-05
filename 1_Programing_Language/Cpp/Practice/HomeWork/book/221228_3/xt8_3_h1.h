// File: xt8_3_h1.h
#include <iostream>
#include <string>

namespace student1 {
    class Student {
    public:
        Student(int n, std::string nam, int a, std::string addr) {
            num = n; name = nam; age = a; address = addr;
        }
        void show_data();
    private:
        int num;
        std::string name;
        int age;
        std::string address;    
    };

    void Student::show_data() {
        std::cout << "num: " << num << " name: " << name << " age: " << age << " address: " << address << std::endl;
    }
}