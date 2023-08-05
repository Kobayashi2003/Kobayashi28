#include "people.h"
// 本练习用于测试新的头文件

using namespace std;

int main() {
    People xiaoming, xiaowang("xiaowang");
    cout << xiaoming << xiaowang;
    xiaoming + 10;
    cout << xiaoming;
    return 0;
}