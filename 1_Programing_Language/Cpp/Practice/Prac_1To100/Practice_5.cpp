// ⼀个班有 n 个学⽣，需要把每个学⽣的简单材料（姓名和
// 学号）输⼊计算机保存。然后可以通过输⼊某⼀学⽣的姓
// 名查找其有关资料。当输⼊⼀个姓名后，程序就查找该班
// 中有⽆此学⽣，如果有，则输出他的姓名和学号，如果查
// 不到，则输出“本班⽆此⼈”。

// 函数 input_data() ⽤来输⼊n个学⽣的姓名和学号
// 函数 search() ⽤来查找要找的学⽣是否在本班

#include<iostream>
#include<string>
#include<map>

using namespace std;

map <string, string> input_data() {
    int num;
    cout << "Enter the number of the students" << endl;
    cin >> num;

    map <string, string> students;

    for(int i = 0; i < num; i++) {
        string name, ID;
        cout << "Enter the name of the student" << endl;
        cin >> name;
        cout << "Enter the ID of the student" << endl;
        cin >> ID;
        students[name] = ID;
    }

    // for(auto p = students.begin(); p != students.end(); p++) {
    //     cout << p -> first << " " << p -> second << endl;
    // }

    return students;
}

void search(map <string, string> &students, string &name) {
    for(auto p = students.begin(); p != students.end(); p++) {
        if(p -> first == name) {
            cout << "The ID of this student is: " << p -> second << endl;
            return;
        }
    }
    cout << "This student is not exit" << endl;
}

int main() {

    map <string, string> students = input_data();

    string name;
    cout << "Enter the name of the student you want to search: " << endl;
    cin >> name;

    search(students, name);

    return 0;
}