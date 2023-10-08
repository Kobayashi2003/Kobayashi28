#include <iostream>
#include <stack>
#include <string>
#include <cmath>
#include <cassert>

using namespace std;

int main() {

    auto priorty = [](char op) {
        switch (op) {
            case '+': return 1;
            case '-': return 1;
            case '*': return 2;
            case '/': return 2;
            case '^': return 3;
            default: return 0;
        }
    };
        

    string expr; cin >> expr;
    stack<int> nums; stack<char> ops;

    for (int i = 0; i < expr.length(); i++) {
        if (expr[i] == ' ') continue;
        if (isdigit(expr[i])) {
            int j = i;
            while (j < expr.length() && isdigit(expr[j])) j++;
            nums.push(stoi(expr.substr(i, j-i)));
            i = j-1;
        } else if (expr[i] == '(') {
            ops.push(expr[i]);
        } else if (expr[i] == ')') {
            while (ops.top() != '(') {
                bool minus = false;

                char op = ops.top(); ops.pop();

                int num2 = nums.top(); nums.pop();
                int num1;
                if (!nums.empty()) {
                    num1 = nums.top(); nums.pop();
                } else if (op == '-') {
                    num1 = 0;
                    minus = true;
                } else {
                    assert(false);
                }
                
                int res;
                switch (op) {
                    case '+': res = num1 + num2; break;
                    case '-': 
                        if (minus) res = -num2;
                        else res = num1 - num2; 
                        break;
                    case '*': res = num1 * num2; break;
                    case '/': res = num1 / num2; break;
                    case '^': res = pow(num1, num2); break;
                }
                nums.push(res);
            }
            ops.pop();
        } else {
            while (!ops.empty() && ops.top() != '(' && priorty(expr[i]) <= priorty(ops.top())) {
                int num2 = nums.top(); nums.pop();
                int num1 = nums.top(); nums.pop();
                char op = ops.top(); ops.pop();
                int res;
                switch (op) {
                    case '+': res = num1 + num2; break;
                    case '-': res = num1 - num2; break;
                    case '*': res = num1 * num2; break;
                    case '/': res = num1 / num2; break;
                    case '^': res = pow(num1, num2); break;
                }
                nums.push(res);
            }
            ops.push(expr[i]);
        }
    }

    while (!ops.empty()) {
        int num2 = nums.top(); nums.pop();
        int num1 = nums.top(); nums.pop();
        char op = ops.top(); ops.pop();
        int res;
        switch (op) {
            case '+': res = num1 + num2; break;
            case '-': res = num1 - num2; break;
            case '*': res = num1 * num2; break;
            case '/': res = num1 / num2; break;
            case '^': res = pow(num1, num2); break;
        }
        nums.push(res);
    }

    cout << nums.top() << endl;

    return 0;
}