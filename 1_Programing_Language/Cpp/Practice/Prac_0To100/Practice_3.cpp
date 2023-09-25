#include<iostream>

typedef int dataType;

using namespace std;

class memberName { // 注意书写顺序
    private :
        dataType mData;
    public :
        memberName(dataType tmData) {
            mData = tmData;
            cout << "Constructor of memberName work" << endl;
        }
        ~memberName() {
            cout << "Destructor of memberName work" << endl;
        }
        void out() {
            cout << mData << endl;
        }
};

class className {
    private :
        dataType data;
        memberName member;
    public :
        className(dataType tData, dataType tmData) : member(tmData) {
            // member前的冒号表示对对象成员的构造函数进行调用（但需要注意，如果该构造函数在类外定义，那么类中的构造函数的声明中，冒号及冒号以后的部分必须略去，并且类外的参数的缺省值去掉）
            // 具体见Practice_4
            data = tData;
            cout << "Constructor of className work" << endl;
        }
        ~className() {
            cout << "Destructor of className work" << endl;
        }
        void out() {
            cout << data << endl;
            member.out();
        }
};

int main() {
    className test(7,9);
    test.out();
    return 0;
}