#include "arrayStack.h"
#include <string>

using namespace std;

void printMatchedPairs(string expr) {

    arrayStack<int> s;
    int length = (int) expr.size();

    for (int i = 0; i < length; i++) 
        if (expr.at(i) == '(')
            s.push(i);
        else
            if (expr.at(i) == ')')
                try {
                    cout << s.top() << ' ' << i << endl;
                    s.pop();
                }
                catch (stackEmpty) {
                    cout << "Unmatched right parenthesis at " << i << endl;
                }
    while (!s.empty()) {
        cout << "Unmatched left parenthesis at " << s.top() << endl;
        s.pop();
    }
}