#include <iostream>
#include "remove_k_digits.h"

int main() {
    // int recods;
    // cin >> recods;
    string num;
    int k;
    // for(int i = 0; i < recods; i++){
    //     string ret = removeKdigits(num, k);
    //     cout << ret << endl;
    // }
    while (cin >> num >> k) {
        string ret = removeKdigits(num, k);
        cout << ret << endl;
    }
    return 0;
}
