// File: xt8_3_h2.h
#include <iostream>
#include <string>

namespace student2 {
    class Student {
    public:
        Student(int n, std::string nam, char s, float sco) {
            num = n; name = nam; sex = s; score = sco;
        } 
        void show_data();
    private:
        int num;
        std::string name;
        char sex;
        float score;
    };
    void Student::show_data() {
        std::cout << "num: " << num << " name: " << name << " sex: " << sex << " score: " << score << std::endl;
    }
};