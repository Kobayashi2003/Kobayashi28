#include<iostream>

using namespace std;

typedef int dataType;

class testTwo;

class testOne {
    private :
        dataType data;
    public :
        testOne(dataType udata) {
            data = udata;
        }
        ~testOne() {}
        void function(testTwo &);
};

class testTwo {
    private :
        dataType data;
    public :
        testTwo(dataType udata) {
            data = udata;
        }
        ~testTwo() {}
        friend void testOne :: function(testTwo &);
};

void testOne :: function(testTwo &obj2) { // 注意函数定义的位置
    cout << "Data1: " << data << endl;
    cout << "Data2: " << obj2.data << endl;
}

int main() {
    testOne one(7);
    testTwo two(9);
    one.function(two);
    return 0;
}