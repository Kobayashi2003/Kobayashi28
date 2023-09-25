// 使用函数重载定义两个重名函数，分别求出int型数的两个点间距离和浮点数的两点间距离。并编写主函数调用该函数，验证。


#include<iostream>

using namespace std;

int distance(const int a, const int b) { return ((a > b) ? (a - b) : (b - a)); }
float distance(const float a, const float b) { return ((a > b) ? (a - b) : (b - a)); }

int main() {
    int a1 = 3, b1 =1;
    float a2 = 3.1, b2 = 1.0;
    cout << distance(a1, b1) << endl;
    cout << distance(a2, b2) << endl;
    return 0;
}