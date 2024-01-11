#include <iostream>
#include <vector>

using namespace std;

struct Node {
    int data;
    Node *left, *right;
};

class BST {
private:
    Node *root = nullptr;
public:
    vector<int> layerCount;

    void insert(int data) {
        Node *newNode = new Node;
        newNode->data = data;
        newNode->left = newNode->right = nullptr;

        if (root == nullptr) {
            root = newNode;
            return;
        }

        Node *cur = root;
        while (cur != nullptr) {
            if (data < cur->data) {
                if (cur->left == nullptr) {
                    cur->left = newNode;
                    return;
                }
                cur = cur->left;
            } else {
                if (cur->right == nullptr) {
                    cur->right = newNode;
                    return;
                }
                cur = cur->right;
            }
        }
    }

    void generateLayerCount() { generateLayerCount(1, root); }

    void generateLayerCount(int layer, Node *cur) {
        if (cur == nullptr) return;
        if (layerCount.size() < layer) layerCount.resize(layer);
        layerCount[layer-1]++;
        generateLayerCount(layer+1, cur->left);
        generateLayerCount(layer+1, cur->right);
    }

    int maxLayer() {
        int max = 0;
        for (int i = 0; i < layerCount.size(); ++i) {
            if (layerCount[i] > max) max = layerCount[i];
        }
        return max;
    }
};


int main() {

    int N; cin >> N;
    while (N--) {
        BST bst;
        int n; cin >> n;
        for (int i = 0; i < n; ++i) {
            int tmp; cin >> tmp;
            bst.insert(tmp);
        }
        bst.generateLayerCount(); 
        cout << bst.maxLayer() << endl;
    }

    return 0;
}