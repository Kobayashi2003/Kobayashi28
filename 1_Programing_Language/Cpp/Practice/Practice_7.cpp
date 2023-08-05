#include<iostream>
#include<string>

using namespace std;

class Student;

class Teacher {
    private :
        int id; string name;
    public :
        Teacher(int uid, string un) {
            id = uid; name = un;
        }
        void assignScore(Student &, float);
};

class Student {
    private :
        int no; string name; float score;
    public :
        Student(int uno, string uname, float uscore) {
            no = uno; name = uname; score = uscore;
        }
        float getScore() {
            return score;
        }
        friend void Teacher::assignScore(Student &, float);
};


void Teacher::assignScore(Student &s, float newScore){
    s.score = newScore;
}

int main() {
    Student ss(1001,"liuMing",75);
    Teacher tt(8801, "laoZhang");
    cout << "Student old Score:" << ss.getScore() << endl;
    tt.assignScore(ss, 87.0f);
    cout << "Student new Score:" << ss.getScore() << endl;
    return 0;
}