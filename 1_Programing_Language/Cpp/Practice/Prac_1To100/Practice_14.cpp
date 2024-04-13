#include<iostream>
#include<cstring>

using namespace std;

typedef int dataType;

class student {
    private :
        char *pName;
    public :
        student() { // 默认的构造函数
            cout << "Constructor";
            pName = NULL;
            cout << "default" << endl;
        }
        student(char *pname);
        student(const student &s); // copy constructor
        ~student();
        student &operator = (student &s); // assignment operator
};

student :: student(char *pname) { // 带参数的构造函数
    cout << "construtor" << endl;
    if(pName = new char[strlen(pname) + 1]) { // 注意：普通的带参数的构造函数也使用了 动态分配 的方法，这是为了防止析构函数中的 delete调用时出错
        strcpy(pName, pname);
    }
    cout << pName << endl;
}

student :: student(const student &s) { // 拷贝构造函数
    cout << "copy constructor" << endl;
    if(pName = new char[strlen(s.pName)]) {
        strcpy(pName, s.pName);
    }
}

student :: ~student() { // 析构函数
    cout << "destructor" << pName << endl;
    if(!pName) delete [] pName;
}

student &student :: operator = (student &s) { // 拷贝赋值操作符）（对运算符 ‘=’ 的重载）
    cout << "copy assignment operator" << endl;
    delete [] pName; // 如果原来
    if(s.pName) {
        if(pName = new char[strlen(s.pName) + 1]) {
            strcpy(pName, s.pName);
        } else {
            pName = NULL;
        }
    }
    return *this;
}

int main() {
    return 0;
}