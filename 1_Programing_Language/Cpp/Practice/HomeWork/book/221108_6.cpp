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
    stud.display();
    stud.change(101, 80.5);
    stud.display();
    
    return 0;
}
