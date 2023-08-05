// 给定一个只包括 '{' '(' '[' '}' ')' ']' 的 字符串，判断该字符串是否有效

#include <iostream>
#include <string>

using namespace std;

const int MAX_SIZE = 1024;

char stack[MAX_SIZE] = {'\0'};
int len = -1;


void push(char item) {
    stack[++len] = item;
}

char pop() {
    return stack[len--];
}

bool judge(string str) {

    for (int i = 0; i < (int)str.length(); ++i) {

        if (str[i] == '(' || str[i] == '{' || str[i] == '[') {

            push(str[i]);

        } else if ( str[i] == ')' ) {

            if (pop() != '(') {
                return false;
            }

        } else if ( str[i] == '}' ) {

            if (pop() != '{') {
                return false;
            }

        } else if ( str[i] == ']' ) {

            if ( pop() != '[' ) {
                return false;
            }

        }
    }
    if (len != -1) {
        return false;
    }
    return true;
}

int main() {

    string str;
    getline(cin, str);
    cout << (judge(str) ? "True" : "False") << endl;

    return 0;
}