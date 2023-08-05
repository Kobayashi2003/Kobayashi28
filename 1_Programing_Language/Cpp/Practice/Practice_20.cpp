#include<iostream>

using namespace std;

void fun(auto & data1, auto & data2) {
    auto tmp = data1;
    data1 = data2;
    data2 = tmp;
}

int main() {
    int a = 1;
    int b = 2;
    fun(a, b);
    cout << a << " " << b << endl;
    return 0;
}