// 5
#include <iostream>

using namespace std;

int main() {
    // int a, b;
    int a, b, c; // 此处应该声明 变量c

    int add(int x, int y); // 函数声明应该放在函数调用处的上方

    cin >> a >> b; // 需要先对 a 与 b 进行赋值才能使用

    // c = add(a, b) // 此处应有分号
    c = add(a, b);

    cout << "a+b=" << c << endl;
    return 0;
}

// int add(int x, int y);
int add(int x, int y) {
    int z; // 应先对 z 进行声明
    z = x + y;
    return z;
}