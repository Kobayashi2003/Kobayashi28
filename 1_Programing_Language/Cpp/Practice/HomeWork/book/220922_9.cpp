// 将三个变量由小到大排列，要求使用引用

#include <iostream>
#include <vector>
#include <algorithm>

void mySort(int &x, int &y, int &z) {
    std::vector<int> v = {x, y, z};
    auto sortByIndex = [](const int &a, const int &b){ return (a<b); }; // 重写排序规则
    std::sort(v.begin(), v.end(), sortByIndex);
    for (auto i : v) {
        std::cout << i << " ";
    }
}

int main() {
    int x, y, z;
    std::cin >> x >> y >> z;
    mySort(x, y, z);
    return 0;
}