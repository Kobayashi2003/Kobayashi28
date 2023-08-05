#include "binomialQueue.h"
#include <iostream>

using namespace std;

int main() {

    BinomialQueue<int> b1;

    // 12 21 24 65 14 26 16 18 23 51 24 65 13
    b1.insert(12);
    b1.insert(21);

    b1.insert(24);
    b1.insert(65);

    b1.insert(14);
    b1.insert(26);

    b1.insert(16);
    b1.insert(18);

    b1.insert(23);
    b1.insert(51);

    b1.insert(24);
    b1.insert(65);

    b1.insert(13);

    cout << "b1: " << endl;
    b1.show();

    cout << endl;

    BinomialQueue<int> b2;

    // 2 11 29 55 15 18 4
    b2.insert(2);
    b2.insert(11);
    b2.insert(29);
    b2.insert(55);
    b2.insert(15);
    b2.insert(18);
    b2.insert(4);

    cout << "b2: " << endl;
    b2.show();

    cout << endl;

    b1.merge(b2);
    cout << "b1.merge(b2): " << endl;
    b1.show();

    return 0;
}