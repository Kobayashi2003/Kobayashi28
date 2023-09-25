#include "myHead.h"

// 此程序旨在观察临时对象的创建与删除

using namespace std;

int main() {

    People xiaoming;
    xiaoming = People("xiaoming", 19); // 在此处程序将会产生一个临时对象用于接收参数,并紧接着将它赋值给xiaoming对象,至于临时对象的析构不同的编译器将会有不同的析构时间
    xiaoming.show();
    return 0;
}