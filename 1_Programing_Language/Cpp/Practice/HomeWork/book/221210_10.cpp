#include <iostream>
#include <string>

using std::string;

class Teacher {
private:
    int num;
    string name;
    char sex;
public:
    Teacher(int n, string na, char s) {
        num = n; name = na; sex = s;
    }

    virtual void show() {
        std::cout << "num: " << num << std::endl;
        std::cout << "name: " << name << std::endl;
        std::cout << "sex: " << sex << std::endl;
    }  
};

class BirthDate {
private:
    int year, month, day;
public:
    BirthDate(int y, int m, int d) {
        year = y; month = m; day = d;
    } 

    void reset(int ny, int nm, int nd) {
        year = ny; month = nm; day = nd;
    } 

    friend std::ostream& operator<<(std::ostream& os, const BirthDate& bd) {
        os << bd.year << "-" << bd.month << "-" << bd.day;
        return os;
    }
};

class Professor : public Teacher {
private:
    BirthDate birth;
public:
    Professor(int n, string na, char s, BirthDate b) : Teacher(n, na, s), birth(b) {}

    void resetBirth(int ny, int nm, int nd) {
        birth.reset(ny, nm, nd);
    }

    void show() {
        Teacher::show();
        std::cout << "birth: " << birth << std::endl;
    } 
};

int main() {
    BirthDate b(1990, 1, 1);
    Professor prof1(1, "zhang", 'm', b); 
    prof1.show();
    prof1.resetBirth(1991, 2, 2);
    prof1.show(); 
    return 0;
} 