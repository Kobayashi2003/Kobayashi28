// 建立一个对象数组，内放 5个 学生的数据（学号，成绩），设立一个函数 max，用指向对象的指针作函数参数，在 max 函数中找出 5个学生中成绩最高者，并输出学号

// 给我五个学号和成绩

#include <iostream>

class Student {
private:
    int _id;
    int _scores;
public:
    Student(int id, int scores) : _id(id), _scores(scores) {}
    Student(const Student& other) : _id(other._id), _scores(other._scores) {}
    int getScores() const { return _scores; }
    int getId() const { return _id; }
    bool operator=(const Student& other) {
        _id = other._id;
        _scores = other._scores;
        return true;
    }
};

int getMaxScore(Student *ss) {
    int max = 0;
    int id = 0;
    for (int i = 0; i < 5; i++) {
        if (ss[i].getScores() > max) {
            max = ss[i].getScores();
            id = ss[i].getId();
        }
    }
    return id;
}

int main() {
    Student ss[5] = {Student(1, 100), Student(2, 90), Student(3, 80), Student(4, 70), Student(5, 60)};
    int max_id = getMaxScore(ss);
    std::cout << max_id << std::endl;
    return 0;
}