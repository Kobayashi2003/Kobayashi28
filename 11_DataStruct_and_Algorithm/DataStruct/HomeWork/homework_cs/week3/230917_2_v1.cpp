#include <iostream>
#include <stack>

using namespace std;

void upstairs(int total) {
    stack<int> s;
    int cur = total; // the cur position
    for (int i = 1; i <= total; ++i)
        s.push(1);

    while (!s.empty()) {

        // if the cur position is equal to total, print the stack
        if (cur == total) {
            stack<int> tmp;
            while (!s.empty()) {
                tmp.push(s.top()); s.pop();
            }
            while (!tmp.empty()) {
                cout << abs(tmp.top()) << " ";
                s.push(tmp.top()); tmp.pop();
            }
            cout << endl;
        }

        if (s.top() == 1) {
            s.pop(); cur -= 1;
            if (cur + 2 <= total) {
                s.push(2); cur += 2;
            }
        } else if (s.top() == 2) {
            s.pop(); 
            if (cur == total) {
                cur -= 2;
                continue;
            }
            s.push(-2); // -2 is a mark, it means that i have already access the '2' in this position
            while (cur < total) {
                s.push(1); cur += 1;
            }
        } else if (s.top() == -2) {
            s.pop(); cur -= 2;
        }
    }
}

int main() {


    int total; cin >> total;
    upstairs(total);

    return 0; 
}