// using stringstream class to receive uncertain number of inputs

// Q:
// the first line of input contains an integer N, standing for the number of lines of input
// the next N lines of input contains uncertain number of integers, you need to output the sum of each line of input

#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {

    int N; cin >> N; cin.ignore();

    string s;
    stringstream ss;
    int sum;
    int num;

    while (N--) {
        getline(cin, s);
        ss.clear();
        ss.str(s);
        sum = 0;
        while (1) {
            ss >> num;
            if (ss.fail()) break;
            sum += num;
        }
        cout << sum << endl;
    }

    return 0;
}