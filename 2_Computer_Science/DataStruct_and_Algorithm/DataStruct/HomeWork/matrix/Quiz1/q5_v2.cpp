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

int dfs(TreeNode* root, vector<vector<int>> &result) {
    if (root == nullptr) return -1;

    int left = dfs(root->left, result);
    int right = dfs(root->right, result);
    int level = max(left, right) + 1;

    if (result.size() == level) {
        result.push_back(vector<int>());
    }

    result[level].push_back(root->val);

    return level;
}

vector<vector<int>> findLeaves(TreeNode* root) {
    vector<vector<int>> result;
    dfs(root, result);
    return result;
}