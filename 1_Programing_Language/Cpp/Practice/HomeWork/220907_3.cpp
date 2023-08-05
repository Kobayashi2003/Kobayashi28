// 输入一行只有加法和乘法的整数算式，计算它的值

// 运算法则 乘法先运算 加法后运算

#include<iostream>

using namespace std;

const int MAX_LEN = 1024;


void Calculator(char *input) {

    int result = 0;
    // first Mult
    for (int i = 0; input[i] != '\0'; ++i) {
        if (input[i] == '*') {
            result += (input[i - 1]-'0') * (input[i + 1]-'0');
            input[i] = input[i + 1] = input[i - 1] = '0';
        }
    }
    // then Add
    for (int i = 0; input[i] != '\0'; ++i) {
        if (input[i] != '+') {
            result += (input[i] - '0');
        }
    }
    cout << result << endl;
}

int main() {

    char input[MAX_LEN] = {'\0'};
    cin.getline(input, MAX_LEN);

    Calculator(input);

    return 0;
}