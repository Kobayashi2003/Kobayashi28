#include <iostream>
#include <string>

using namespace std;

void GetPreOrder(string inOrder, string postOrder, string & preOrder) {
    if (inOrder.length() == 0) return;
    if (inOrder.length() == 1) {
        preOrder += inOrder[0];
        return;
    }

    char root = postOrder[postOrder.length() - 1];
    preOrder += root;

    int rootIndex = inOrder.find(root);
    string leftInOrder = inOrder.substr(0, rootIndex);
    string rightInOrder = inOrder.substr(rootIndex + 1, inOrder.length() - rootIndex - 1);

    int leftLength = leftInOrder.length();
    int rightLength = rightInOrder.length();

    string leftPostOrder = postOrder.substr(0, leftLength);
    string rightPostOrder = postOrder.substr(leftLength, rightLength);

    GetPreOrder(leftInOrder, leftPostOrder, preOrder);
    GetPreOrder(rightInOrder, rightPostOrder, preOrder);
}

int main() {

    string inOrder; cin >> inOrder;
    string postOrder; cin >> postOrder;

    string preOrder = "";

    GetPreOrder(inOrder, postOrder, preOrder);

    cout << preOrder << endl;

    return 0;
}