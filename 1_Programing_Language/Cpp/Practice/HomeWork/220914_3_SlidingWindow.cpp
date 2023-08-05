#include <iostream>
#include <set>

using namespace std;

const int MAX_LEN = 1024;

int main() {

    char input[MAX_LEN] = {'\0'};
    cin.getline(input, MAX_LEN);


    // sliding window
    int cont = 0, tmp = 0;
    set <char> table;
    // define the front and back of window
    for (int front = 0, back = 0; input[front] != '\0'; ++front) {
        if (table.find(input[front]) != table.end()) {
            do { // move the back of window to make the front of window confirm the rule
                table.erase(input[back]);
                back += 1;
                tmp -= 1;
            } while (input[back-1] != input[front]);
        }
        // If the current element does not exist in the list, insert it into set for subsequent inspection
        table.insert(input[front]);
        tmp += 1;
        // recording the maximum length in all substrings
        cont = (cont < tmp ? tmp : cont);
    }
    cout << cont << endl;

    return 0;
}