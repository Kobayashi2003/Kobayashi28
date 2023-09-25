#include <iostream>
#include <stack>
#include <string>

using namespace std;

class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty()) return false;
                char top = st.top();
                if (c == ')' && top != '(') return false;
                if (c == ']' && top != '[') return false;
                if (c == '}' && top != '{') return false;
                st.pop();
            }
        }
        if (st.empty()) return true;
        return false;
    }
};


int main() {

    string s = "()[]{}";
    Solution solution;
    cout << solution.isValid(s) << endl;

    return 0;
}