#include <iostream>

class Student {
private:
    int num;
    float score;
public:
    Student(int n, float s) : num(n), score(s) {}
    void change(int n, float s) { num = n; score = s; }
    void display() { std::cout << num << " " << score << std::endl; }
};

int main() {

    Student stud(101, 78.5);
    Student * const p = &stud;
    // const Student * p = &stud; 
    p->display();
    p->change(101, 80.5);
    p->display();

    return 0;
}
