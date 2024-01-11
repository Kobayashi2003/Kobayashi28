#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class Solution {

private:

    vector<int> power;
    vector<pair<int, int>> tree;
    vector<bool> isSymmetric;

public:

    Solution() {
        int n; cin >> n;
        power.resize(n);
        tree.resize(n);
        isSymmetric.resize(n);
        for (int i = 0; i < n; i++) {
            cin >> power[i];
        }
        for (int i = 0; i < n; i++) {
            int lchild, rchild; cin >> lchild >> rchild;
            if (lchild > 0) lchild--;
            if (rchild > 0) rchild--;
            tree[i] = make_pair(lchild, rchild);
        }
    }

    int getPower(int root) {
        if (root == -1) return 0;
        return power[root] + getPower(tree[root].first) + getPower(tree[root].second);
    }

    bool checkSymmetricTree (int root = 0) {
        if (root == -1) return true;
        if (tree[root].first == -1 && tree[root].second == -1) {
            isSymmetric[root] = true;
            return true;
        }
        if (tree[root].first == -1 || tree[root].second == -1) {
            isSymmetric[root] = false;
            return false;
        }
        if (checkSymmetricTree(tree[root].first) && checkSymmetricTree(tree[root].second)) {
            if (getPower(tree[root].first) == getPower(tree[root].second)) {
                isSymmetric[root] = true;
                return true;
            }
        }
        isSymmetric[root] = false;
        return false;
    }

    int findBiggestSymTree() {
        int Max = 0;
        for (int i = 0; i < tree.size(); i++) {
            if (isSymmetric[i]) {
                int countNodes = 0;
                queue<int> q;
                q.push(i);
                while (!q.empty()) {
                    int root = q.front();
                    q.pop();
                    countNodes++;
                    if (tree[root].first != -1) q.push(tree[root].first);
                    if (tree[root].second != -1) q.push(tree[root].second);
                }
                if (countNodes > Max) Max = countNodes;
            }
        }
        return Max;
    }
};


int main() {

    Solution solution;
    solution.checkSymmetricTree();
    cout << solution.findBiggestSymTree() << endl;

    return 0;
}