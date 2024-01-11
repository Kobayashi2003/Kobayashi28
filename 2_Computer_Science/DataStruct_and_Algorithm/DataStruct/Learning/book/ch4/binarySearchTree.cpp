#include "binarySearchTree.h"
#include <iostream>

using namespace std;

int main() {

    binarySearchTree<int> *p = new binarySearchTree<int>(3);
    p->insert(1);
    p->insert(4);
    p->insert(6);
    p->insert(9);
    p->insert(2);
    p->insert(5);
    p->insert(7);

    p->preOrder();
    cout << endl;
    p->inOrder();
    cout << endl;
    p->postOrder();
    cout << endl;

    p->remove(1);
    p->preOrder();
    cout << endl;
    p->inOrder();
    cout << endl;
    p->postOrder();
    cout << endl;


    return 0;
}