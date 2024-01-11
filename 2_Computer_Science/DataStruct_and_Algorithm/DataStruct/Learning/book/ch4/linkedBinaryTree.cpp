#include <iostream>
#include "linkedBinaryTree.h"

int main() {

    linkedBinaryTree<int> bt1(1);
    linkedBinaryTree<int> bt2(2);
    linkedBinaryTree<int> bt3(3);

    bt1.makeTree(1, bt2, bt3);

    bt1.preOrder();
    std::cout << std::endl;
    bt1.inOrder();
    std::cout << std::endl;
    bt1.postOrder();
    std::cout << std::endl;

    auto visit = [](linkedBinaryTree<int>::Node *t) { std::cout << t->data + 1 << " "; };
    bt1.preOrder(visit);

    return 0;
}