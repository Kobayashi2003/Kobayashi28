#include <iostream>
#include <vector>
#include <stack>

using namespace std;

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> s;
        for (auto &token : tokens) {
            if (token == "+" || token == "-" || token == "*" || token == "/") {
                int num2 = s.top(); s.pop();
                int num1 = s.top(); s.pop();
                if (token == "+") s.push(num1 + num2);
                else if (token == "-") s.push(num1 - num2);
                else if (token == "*") s.push(num1 * num2);
                else s.push(num1 / num2);
            } else {
                s.push(stoi(token));
            }
        }
        return s.top(); 
    }
};

int main() {
    Solution sol;
    vector<string> tokens = {"2", "1", "+", "3", "*"};
    cout << sol.evalRPN(tokens) << endl;
    return 0;
}