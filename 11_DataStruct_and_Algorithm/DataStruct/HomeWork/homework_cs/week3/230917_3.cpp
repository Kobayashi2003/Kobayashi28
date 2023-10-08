#include <iostream>
#include <string>
#include <cmath>
#include <stack>
#include <regex>
#include <cassert>

using namespace std;

int PRIORTY(char op) {
    switch (op) {
        case '+': return 1;
        case '-': return 1;
        case '*': return 2;
        case '/': return 2;
        case '^': return 3;
        default: return 0;
    }
}

double calculate(string expr) {
    stack<double> nums;
    stack<char> ops;
    int len = expr.size();
    for (int i = 0; i < len; ++i) {
        if (expr[i] == ' ') continue;
        if (isdigit(expr[i])) {
            int j = i;
            while (j < len && isdigit(expr[j])) ++j;
            nums.push(stod(expr.substr(i, j-i)));
            i = j-1;
        } else if (expr[i] == '(') {
            ops.push(expr[i]);
        } else if (expr[i] == ')') {
            while (ops.top() != '(') {
                double num2 = nums.top(); nums.pop();
                double num1 = nums.top(); nums.pop();
                char op = ops.top(); ops.pop();
                double res;
                switch (op) {
                    case '+': res = num1 + num2; break;
                    case '-': res = num1 - num2; break;
                    case '*': res = num1 * num2; break;
                    case '/': res = num1 / num2; break;
                    case '^': res = pow(num1, num2); break;
                }
                nums.push(res);
            }
            ops.pop();
        } else {
            while (!ops.empty() && ops.top() != '(' && PRIORTY(expr[i]) <= PRIORTY(ops.top())) {
                double num2 = nums.top(); nums.pop();
                double num1 = nums.top(); nums.pop();
                char op = ops.top(); ops.pop();
                double res;
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
        double num2 = nums.top(); nums.pop();
        double num1 = nums.top(); nums.pop();
        char op = ops.top(); ops.pop();
        double res;
        switch (op) {
            case '+': res = num1 + num2; break;
            case '-': res = num1 - num2; break;
            case '*': res = num1 * num2; break;
            case '/': res = num1 / num2; break;
            case '^': res = pow(num1, num2); break;
        }
        nums.push(res);
    }
    assert(nums.size() && ops.size() == 0);
    return nums.top();
}


int main() {

    // for integer expression
    
    /*example
    > input the expression: 
    > ((x+2)^2 - 4) / 4
    > input the value of variable:
    > x = 2

    then the expression will be changed to:
    > ((2+2)^2 - 4) / 4
    then the calculator will calculate the expression and print the result:
    > the result is: 3
    */

    cout << "input the expression: " << endl;
    string expr; getline(cin, expr);
    cout << "input the value of variable:\n(if there are more than one variable, please use ',' or ' ' to split) " << endl;
    string vars; getline(cin, vars);
    // x = 2, y=3 z = 4
    regex reg("[a-zA-Z] *= *[0-9]+"); // search the variable and its value
    smatch sm;
    stack<string> st;
    while (regex_search(vars, sm, reg)) {
        st.push(sm[0]);
        vars = sm.suffix();
    }
    while (!st.empty()) {
        string tmp = st.top(); st.pop();
        regex reg2("[a-zA-Z]"); // search the variable
        smatch sm2;
        regex_search(tmp, sm2, reg2);
        string var = sm2[0];

        regex reg3("[0-9]+"); // search the value
        smatch sm3;
        regex_search(tmp, sm3, reg3);
        string val = sm3[0];

        regex reg4(var);
        expr = regex_replace(expr, reg4, val);
    }
    cout << "the expression will be changed to: " << endl;
    cout << expr << endl;

    cout << "the result is: " << endl;
    cout << calculate(expr) << endl;

    return 0;
}