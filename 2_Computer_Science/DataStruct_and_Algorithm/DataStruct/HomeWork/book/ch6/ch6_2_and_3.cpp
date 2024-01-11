#include "binaryHeap.h"
#include <iostream>

using namespace std;

int main() {

    vector<int> v = { 10, 12, 1, 14, 6, 5, 8, 15, 3, 9, 7, 4, 11, 13, 2 };

    // question 6.2 a
    BinaryHeap<int> bh1; bh1.makeEmpty();
    for (int i = 0; i < v.size(); ++i)
        bh1.insert(v[i]);
    cout << "question 6.2 a" << endl;
    bh1.showHeap();


    cout << endl;
    

    // question 6.2 b
    BinaryHeap<int> bh2(v);
    cout << "question 6.2 b" << endl;
    bh2.showHeap();


    cout << endl;


    // question 6.3 a
    for (int i = 0; i < 3; ++i)
        bh1.deleteMin();
    cout << "question 6.3 a" << endl;
    bh1.showHeap();


    cout << endl;


    // question 6.3 b
    for (int i = 0; i < 3; ++i)
        bh2.deleteMin();
    cout << "question 6.3 b" << endl;
    bh2.showHeap();


    return 0;
}