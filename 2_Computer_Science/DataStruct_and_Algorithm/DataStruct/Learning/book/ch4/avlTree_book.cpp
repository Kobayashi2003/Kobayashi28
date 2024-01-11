#include "avlTree_book.h"
#include <iostream>
#include <random>

using namespace std;

int main() {

    AvlTree<int> t;
    int NUMS = 4000;
    
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(1, 100000);

    for (int i = 0; i < NUMS; ++i)
        t.insert(dis(gen));
        

    t.preOrder();
    cout << endl;
    t.inOrder();

    return 0;
}