#include "countingRadixSort.hpp"
#include <vector>
#include <string>
#include <iostream>

using namespace std;

int main() {
    vector<string> vs = {"CCC", "BBB", "ABC", "DBE", "AAA", "CAB"};
    contingRradixSort(vs, 3);
    for (auto &s : vs) {
        cout << s << endl;
    }
    return 0;
}