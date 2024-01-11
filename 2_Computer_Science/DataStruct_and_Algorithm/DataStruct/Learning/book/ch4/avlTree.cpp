#include "avlTree.h"
#include <iostream>
#include <random>


int main() {

    avlTree<int> t;
    int NUMS = 4000;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100000);

    for (int i = 0; i < NUMS; ++i)
        t.insert(dis(gen));

    t.preOrder();
    std::cout << std::endl;
    t.inOrder();

    return 0;
}