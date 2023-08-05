// lambda表达式的使用例

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::for_each(v.begin(), v.end(), [](int n) {std::cout << n << " ";});
    std::cout << std::endl;
    return 0;
}