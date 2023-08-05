#include <iostream>
#include <stack>

using namespace std;

bool checkBox(int net[], int n) {
    auto s = new stack<int>();
    for (int i = 0; i < n; ++i) {
        if (!s->empty())
            if (net[i] == net[s->top()]) 
                s->pop();
            else
                s->push(net[i]);
        else
            s->push(net[i]);
    }

    if (s->empty())
        return true;
    else
        return false;
}

int main() {
    int net1[] = {3, 2, 1, 0, 5, 4, 7, 6};
    if (checkBox(net1, 8))
        cout << "true" << endl;
    else
        cout << "false" << endl;
    int net2[] = {4, 2, 1, 6, 0, 7, 3, 5};
    if (checkBox(net2, 8))
        cout << "true" << endl;
    else
        cout << "false" << endl;
    return 0;
}