#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

int main() {

    string preOrder, postOrder;
    cin >> preOrder >> postOrder;

    int type = 1;

    int n = preOrder.size();
    for (int i = 1; i < n; ++i) {
        int index = postOrder.find(preOrder[i]);
        if (postOrder[index + 1] == preOrder[i - 1]) {
            type *= 2;
        }
    }

    cout << type << endl;   

    return 0;
}