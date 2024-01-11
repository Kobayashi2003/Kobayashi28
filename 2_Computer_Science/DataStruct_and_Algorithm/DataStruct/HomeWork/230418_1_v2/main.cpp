#include <iostream>
#include <string>

#include "AVLtree.h"
using namespace std;

int main() {
    int data_in;
    AVLtree<int> avltree;
    while (std::cin >> data_in) {
        avltree.insert(data_in);
        if (std::cin.get() == '\n') break;
    }
    avltree.preOrder();
    return 0;
}