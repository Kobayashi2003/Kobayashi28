#include<iostream>

const int MAX_LEN = 1024;

using namespace std;

int main() {

    char equ_str[MAX_LEN] = {'\0'};
    cin.getline(equ_str, MAX_LEN);

    int sum = 0, num = 0, mul = -1;
    for (int i = 0; equ_str[(i==0 ? 0 : i-1)] != '\0'; ++i) {

        if (equ_str[i] >= '0' && equ_str[i] <= '9') {
            // Change qualified strings to numbers
            num = num * 10 + (equ_str[i] - '0');

        } else if (equ_str[i] == '*') {
            // When '*' is encountered,store the data in {mul}
            mul = (mul == -1 ? num : mul*num);
            num = 0;

        } else {
            // Accumulator
            sum += (mul == -1 ? num : (mul * num));
            num = 0; mul = -1;
            
        }
    }
    cout << sum << endl;

    return 0;
}