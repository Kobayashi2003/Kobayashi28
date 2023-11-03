#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool judgeBST(vector<int> preOrder, vector<int> inOrder) {

    if (preOrder.size() == 0) return true;

    int root = preOrder[0];
    int rootIndex = find(inOrder.begin(), inOrder.end(), root) - inOrder.begin();

    vector<int> leftPreOrder(preOrder.begin() + 1, preOrder.begin() + rootIndex + 1);
    vector<int> rightPreOrder(preOrder.begin() + rootIndex + 1, preOrder.end());
    vector<int> leftInOrder(inOrder.begin(), inOrder.begin() + rootIndex);
    vector<int> rightInOrder(inOrder.begin() + rootIndex + 1, inOrder.end());

    for (int i = 0; i < leftPreOrder.size(); ++i) {
        if (root < leftPreOrder[i]) return false;
    }

    for (int i = 0; i < rightPreOrder.size(); ++i) {
        if (root > rightPreOrder[i]) return false;
    }

    return judgeBST(leftPreOrder, leftInOrder) && judgeBST(rightPreOrder, rightInOrder);
}

int main() {

    int N; cin >> N;

    for (int i = 0; i < N; ++i) {
        int n; cin >> n;
        vector<int> preOrder(n), inOrder(n);
        for (int i = 0; i < n; ++i) cin >> preOrder[i];
        for (int i = 0; i < n; ++i) cin >> inOrder[i];
        cout << (judgeBST(preOrder, inOrder) ? "Yes" : "No") << endl;
    }
    
    return 0;
}