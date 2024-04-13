#include<iostream>
#include<string>

using namespace std;

class People {
private :
    string name;
    int age;
    char sex;
public :
    People(string tname = "xiao ming", int tage = 18, char tsex = 'M');
    ~People() {};
    void show() {
        cout << "name: " << name << endl << "age: " << age << endl << "sex: " << sex << endl;
    }
};

People :: People(string tname, int tage, char tsex) {
    name = tname; age = tage; sex = tsex;
}

int main() {
    People xiaoming;
    xiaoming.show();

    People xiaowang("xiao wang");
    xiaowang.show();
    return 0;
}