#include <iostream>
#include <memory>

using namespace std;

// share pointer
// 如果程序要使用多个指向同一个对象的指针，应选择 shared_ptr
void demo1() {
    shared_ptr<int> p1(new int(10));
    cout << "p1 = " << *p1 << endl;
    shared_ptr<int> p2(p1);
    cout << "p2 = " << *p2 << endl;
    cout << "p1 = " << *p1 << endl;
    cout << "p1.use_count() = " << p1.use_count() << endl;
    cout << "p2.use_count() = " << p2.use_count() << endl;
    p1.reset();
    cout << "p1.use_count() = " << p1.use_count() << endl;
    cout << "p2.use_count() = " << p2.use_count() << endl;
    cout << "p2 = " << *p2 << endl;
}

// unique pointer
// 如果程序要使用单个指向某个对象的指针，可以选择选择 unique_ptr
void demo2() {
    unique_ptr<int> p1(new int(10));
    cout << "p1 =" << *p1 << endl;
    unique_ptr<int> p2(move(p1));
    cout << "p2 =" << *p2 << endl;
}



int main() {
    // cout << "----demo1----" << endl;
    // demo1();
    // cout << "----demo2----" << endl;
    // demo2();

    

    return 0;
}