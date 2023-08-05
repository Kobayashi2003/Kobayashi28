// 栈的 FILO 问题

#include<iostream>

using namespace std;

char stack[8] = {'\0'};
int top = -1;
char x = 'A';

void pop() {
    stack[top--] = '\0';
}

void push(char data) {
    stack[++top] = data;
}

bool isNotEmpty() {
    if (top == -1) {
        return false;
    }
    return true;
}

int main() {

    char testData[8] = {'\0'};
    cin.getline(testData, 9);

    int i = 0;
    while (i < 8) {
        if (isNotEmpty() && stack[top] == testData[i]) {
            pop();
            i += 1;
        } else {
            if (x <= 'H') {
                push(x++);
            } else {
                break;
            }
        }
    }

    if (isNotEmpty()) {
        cout << 0 << endl;
    } else {
        cout << 1 << endl;
    }

    return 0;
}