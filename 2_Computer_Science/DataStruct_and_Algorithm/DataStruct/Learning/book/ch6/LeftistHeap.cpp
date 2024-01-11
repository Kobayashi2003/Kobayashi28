#include "LeftistHeap.h"

using namespace std;

int main() {

    LeftistHeap<int> lh1;
    LeftistHeap<int> lh2;

    // lh1 insert 3 10 8 21 14 17 23 26
    lh1.insert(3);
    lh1.insert(10);
    lh1.insert(8);
    lh1.insert(21);
    lh1.insert(14);
    lh1.insert(17);
    lh1.insert(23);
    lh1.insert(26);

    // lh2 insert 6 12 7 18 24 37 18 33
    lh2.insert(6);
    lh2.insert(12);
    lh2.insert(7);
    lh2.insert(18);
    lh2.insert(24);
    lh2.insert(37);
    lh2.insert(18);
    lh2.insert(33);

    // lh1 merge lh2
    lh1.merge(lh2);

    return 0;
}