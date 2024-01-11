#include <iostream>
#include <math.h>
#include <stack>
#include <string>
using namespace std;

stack<char> symbol_stack;
stack<int> number_stack;

//从数字栈中取出栈顶的两个数字进行相关运算，结果放入栈中
void math(char f) {
	// 请完成匹配函数代码
    int a = number_stack.top();
    number_stack.pop();
    int b = number_stack.top();
    number_stack.pop();
    int c;
    switch (f) {
        case '+':
            c = b + a;
            break;
        case '-':
            c = b - a;
            break;
        case '*':
            c = b * a;
            break;
        case '/':
            c = b / a;
            break;
    }
    number_stack.push(c);
}

int main() {
	string str;
	getline(cin, str);
	int number = 0;


	// 请完成主函数代码
    for (size_t i = 0; i < str.size(); ++i) {
        if (str[i] >= '0' && str[i] <= '9') {
            number = number * 10 + str[i] - '0';
            if (i == str.size() - 1 || str[i+1] < '0' || str[i+1] > '9') {
                number_stack.push(number);
                number = 0;
            }
        } else {

            switch (str[i]) {
                case ')':
                    while (symbol_stack.top() != '(') {
                        math(symbol_stack.top());
                        symbol_stack.pop();
                    }
                    symbol_stack.pop();
                    break;
                case '(': case '*': case '/':
                    symbol_stack.push(str[i]);
                    break;
                case '+': case '-':
                    while (!symbol_stack.empty() &&  symbol_stack.top() != '(') {
                        math(symbol_stack.top());
                        symbol_stack.pop();
                    }
                    symbol_stack.push(str[i]);
                    break;
                default:
                    continue;
            }
        }
    }
    while (!symbol_stack.empty()) {
        math(symbol_stack.top());
        symbol_stack.pop();
    }

	cout << number_stack.top() << endl;
	return 0;
}