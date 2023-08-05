// 建立一个对象数组，内放 5个 学生的数据（学号，成绩），用指针指向数组首元素，输出第 1，3，5 个学生的数据

#include <iostream>

class Student {
private:
    int _id;
    int _scores;
public:
    Student(int id=0, int scores=0);
    void set(int id, int scores);
    void show(int index=0) const;
};

Student::Student(int id, int scores) : _id(id), _scores(scores) {}

void Student::set(int id, int scores) {
    _id = id; _scores = scores;
}

void Student::show(int index) const {
    std::cout << "Student ID: " << _id << std::endl;
    std::cout << "Scores: " << _scores << std::endl;
}

int main() {
    auto *ss = new Student[5];
    for (int i = 0; i < 5; ++i) {
        ss[i].set(i, 40 + 5*i);
    }
    ss[0].show(); ss[2].show(); ss[4].show();
    return 0;
}