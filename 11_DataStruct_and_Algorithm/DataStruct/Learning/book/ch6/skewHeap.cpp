#include <iostream>
#include "skewHeap.h"

using namespace std;


int main() {


    SkewHeap<int> sh1;
    SkewHeap<int> sh2;

    // sh1 insert 3 10 8 21 14 17 23 26
    sh1.insert(3);
    sh1.insert(10);
    sh1.insert(8);
    sh1.insert(21);
    sh1.insert(14);
    sh1.insert(17);
    sh1.insert(23);
    sh1.insert(26);

    // sh2 insert 6 12 7 18 24 37 18 33
    sh2.insert(6);
    sh2.insert(12);
    sh2.insert(7);
    sh2.insert(18);
    sh2.insert(24);
    sh2.insert(37);
    sh2.insert(18);
    sh2.insert(33);

    // sh1 merge sh2
    sh1.merge(sh2);

    return 0;
}