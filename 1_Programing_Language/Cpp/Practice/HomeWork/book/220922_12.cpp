// 有 5 个字符串，要求对它们从小到大进行排序，要求使用 string 方法

#include <iostream>
#include <string>
using namespace std;

int main() {
    string strs[5];
    for (int i = 0; i < 5; ++i) {
        getline(cin, strs[i]);
    }
    for (int i = 0; i < 5; ++i) {
        string &min = strs[i];
        for (int j = i; j < 5; ++j) {
            if (min > strs[j]) {
                min.swap(strs[j]); // 使用 swap方法调换两字符串
            }
        }
    }
    for (int i = 0; i < 5; ++i) {
        cout << strs[i] << endl;
    }
    return 0;
}