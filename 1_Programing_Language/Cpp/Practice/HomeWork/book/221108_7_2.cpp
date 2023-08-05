#include <iostream>

class Student {
private:
    mutable int num;
    mutable float score;
public:
    Student(int n, float s) : num(n), score(s) {}
    void change(int n, float s) const { num = n; score = s; }
    void display() const { std::cout << num << " " << score << std::endl; }
};

int main() {

    const Student stud(101, 78.5);
    stud.display();
    stud.change(101, 80.5);
    stud.display();

    return 0;
}
