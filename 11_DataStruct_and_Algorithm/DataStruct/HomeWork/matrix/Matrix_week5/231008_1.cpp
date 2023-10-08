#include <iostream>
#include <algorithm>
#include <string>
#include <stack>


using namespace std;

class Solution {
private:
    stack<int> s;
    int min = INT_MAX;
public:

    Solution() { } 

    void StackOpt(int opt, int x = 0) {
        switch (opt) {
            case 0:
                s.push(x);
                if (x < min) min = x;
                break;
            case 1:
                if (!s.empty()) s.pop();

                if (s.empty()) min = INT_MAX;
                else {
                    stack<int> tmp;
                    min = INT_MAX;
                    while (!s.empty()) {
                        int t = s.top();
                        tmp.push(t);
                        if (t < min) min = t;
                        s.pop();
                    }
                    while (!tmp.empty()) {
                        s.push(tmp.top());
                        tmp.pop();
                    }
                }
                break;
            case 2:
                cout << (s.empty() ? -1 : s.top()) << endl;
                break;
            case 3:
                cout << (s.empty() ? -1 : min) << endl;
                break;
            default:
                return;
        }
    }
};

int main() {

    string s;
    bool flg = false;
    while (getline(cin, s)) {
        if (s.size() == 0) {
            if (flg) break;
            else {
                flg = true;
                continue;
            }
        }
        flg = false;

        int n = stoull(s);
        Solution sol;
        for (int i = 0; i < n; ++i) {
            getline(cin, s);
            int opt = stoi(s.substr(0, 1));
            if (opt == 0) {
                int x = stoull(s.substr(2));
                sol.StackOpt(opt, x);
            } else {
                sol.StackOpt(opt);
            }
        }
    }

    return 0;
}