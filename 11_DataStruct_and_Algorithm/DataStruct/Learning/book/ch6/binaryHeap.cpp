#include "binaryHeap.h"
#include <iostream>
#include <random>

using namespace std;

int main() {

    vector<int> v;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(1, 99);
    for (int i = 0; i < 10; ++i) {
        v.push_back(dis(gen));
    }

    BinaryHeap<int> bh(v);
    cout << "bh: ";
    while (!bh.isEmpty()) {
        cout << bh.findMin() << " ";
        bh.deleteMin();
    }
    cout << endl;

    return 0;
}