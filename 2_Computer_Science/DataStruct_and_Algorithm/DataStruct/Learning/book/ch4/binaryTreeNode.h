#ifndef BINARYTREENODE_H
#define BINARYTREENODE_H

template <typename Object>
struct binaryTreeNode {
    Object data;
    binaryTreeNode* left;
    binaryTreeNode* right;
    int height;
    binaryTreeNode() :left(nullptr), right(nullptr), height(0) {}
    binaryTreeNode(Object item, binaryTreeNode* L = nullptr, binaryTreeNode* R = nullptr) :data(item), left(L), right(R), height(0) {}
};

#endif