#include<iostream>
#include<new>

// 本练习用于演示定位new运算符

using namespace std;

struct chaff {
    char dross[20];
    int slag;
};
char buffer1[50];
char buffer2[500];

int main() {
    chaff *p1, *p2;
    int *p3, *p4;
// first: the regular forms of new
    p1 = new chaff; // place structure in heap
    p3 = new int[20]; // place int array in heap;
//  now, the two forms of placement new
    p2 = new (buffer1) chaff; // place structure in buffer1
    p4 = new (buffer2) int[20]; // place int array in buffer2
    cout << "buffer1: " << &buffer1 << endl << "buffer2: " << &buffer2 << endl;
    cout << "p1: " << p1 << endl << "p3: " << p3 << endl;
    cout << "p2: " << p2 << endl << "p4: " << p4 << endl;
    return 0;
}

// result:

// buffer1: 0x7ff64a3d9040
// buffer2: 0x7ff64a3d9080
// p1: 0x212fdae17d0
// p3: 0x212fdae3ae0
// p2: 0x7ff64a3d9040
// p4: 0x7ff64a3d9080

// 可见，使用定位new能够让我们访问到特定的地址