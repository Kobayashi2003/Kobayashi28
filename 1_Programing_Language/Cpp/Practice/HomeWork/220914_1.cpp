#include <iostream>

using namespace std;

const int MAX_LEN = 1024;

int main() {
    char input[MAX_LEN] = {'\0'};
    cin.getline(input, MAX_LEN);
    for (int i = 0; input[i] != '\0'; ++i) {
        if (input[i] == ',') {
            cout << endl;
        } else {
            cout << input[i];
        }
    }
    return 0;
}