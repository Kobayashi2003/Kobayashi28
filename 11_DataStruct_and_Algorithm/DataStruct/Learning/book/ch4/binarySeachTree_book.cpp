#include "binarySeachTree_book.h"
#include <iostream>

using namespace std;

int main() {

    BinarySearchTree<int> bst;
    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    bst.insert(2);
    bst.insert(4);
    bst.insert(6);
    bst.insert(8);

    bst.printTree();


    return 0;
}