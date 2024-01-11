#include <iostream>
#include <vector>

using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

vector<vector<int>> findLeaves(TreeNode* root);

void preOrder(TreeNode* root, vector<int> &leaves) {
    if (root == nullptr) return;

    if (root->left == nullptr && root->right == nullptr) {
        leaves.push_back(root->val);
        return;
    }

    preOrder(root->left, leaves);
    preOrder(root->right, leaves);
}

void removeLeaves(TreeNode *&root) {
    if (root == nullptr) return;
    if (root->left == nullptr && root->right == nullptr) {
        delete root;
        root = nullptr;
        return;
    }

    if (root->left != nullptr && root->left->left == nullptr && root->left->right == nullptr) {
        delete root->left;
        root->left = nullptr;
    }

    if (root->right != nullptr && root->right->left == nullptr && root->right->right == nullptr) {
        delete root->right;
        root->right = nullptr;
    }

    removeLeaves(root->left);
    removeLeaves(root->right);
}

vector<vector<int>> findLeaves(TreeNode* root) {
    vector<vector<int>> result;

    while (root != nullptr) {
        vector<int> leaves;
        preOrder(root, leaves);
        result.push_back(leaves);
        removeLeaves(root);
    }

    return result;
}