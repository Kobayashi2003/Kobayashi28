#include<iostream>
#include<map>
#include<string>

using namespace std;

class Dic {
private:
    map <string, string> dic;
public:
    Dic() {}
    ~Dic() {}

    void add(string Eng, string Chi);
    void trans(string sen);
};

void Dic::add(string Eng, string Chi) {
    dic[Eng] = Chi;
}

void Dic::trans(string sen) {
    if (sen == "") {
        return;
    }
    int i = 0;
    string tmp = "";
    while (sen[i] != '\0') {
        if (sen[i] == ' ') {
            cout << dic[tmp];
            tmp = "";
        } else {
            tmp += sen[i];
        }
        i++;
    }
    cout << dic[tmp] << endl;
}

int main() {
    Dic d;
    d.add("a", "一个");
    d.add("I", "我");
    d.add("am", "是");
    d.add("student", "学生");
    d.add("teacher", "老师");
    d.trans("I am a student");    // 我是一个学生（输出结果）
    d.trans("I am a teacher");    // 我是一个老师（输出结果）
    return 0;
}