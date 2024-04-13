// :: 运算符的使用
// 全局作用域符号

#include<iostream>
#include<string>

using namespace std;

string data = "Global";

void function(string data) {
    cout << "global: " << :: data << endl;
    cout << "local: " << data << endl;
}

int main() {
    function("Local");
    return 0;
}