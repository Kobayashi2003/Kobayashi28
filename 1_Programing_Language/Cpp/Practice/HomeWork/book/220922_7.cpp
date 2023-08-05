// 求 2个 或 3个 正整数中的最大数，用带有默认参数的函数实现

#include <iostream>

using namespace std;

int Max(int x, int y, int z = -1) {
    int max_tmp = x > y ? x : y; // 比较 x与y，将较大者赋值于max_tmp
    if (z != -1) {
        max_tmp = max_tmp > z ? max_tmp : z; // 比较 max_tmp与z，将较大者赋值于max_tmp
    }
    return max_tmp;
}

int main() {
    int x = 11, y = 1, z = 17;
    cout << "the max in x, y, z is: " << Max(x, y, z) << endl;
    cout << "the max in x, y is: " << Max(x, y) << endl;
    return 0;
}