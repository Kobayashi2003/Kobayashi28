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

void fun(Student &stud) {
    stud.change(101, 80.5);
    stud.display();
}

int main() {

    Student stud(101, 78.5);
    stud.display();
    fun(stud);
    
    return 0;
}
