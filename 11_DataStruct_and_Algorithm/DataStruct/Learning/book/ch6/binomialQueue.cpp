#include "binomialQueue.h"
#include <iostream>

using namespace std;

int main() {

    BinomialQueue<int> a;
    BinomialQueue<int> b;

    a.insert(1);
    a.insert(2);
    a.insert(3);


    b.insert(4);
    b.insert(5);
    b.insert(6);

    a.merge(b);

    return 0;
}