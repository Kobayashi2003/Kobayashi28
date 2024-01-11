#include "find_leaves.h"

vector<vector<int>> res;

int dfs(TreeNode* node) {
    if (!node) return -1;

    // 左
    int left = dfs(node->left);
    // 右
    int right = dfs(node->right);
    // 本结点
    int curr = max(left, right) + 1;
    if (curr >= res.size()) res.push_back({});
    res[curr].push_back(node->val);
    return curr;
}

vector<vector<int>> findLeaves(TreeNode* root) {
    dfs(root);
    return res;
}