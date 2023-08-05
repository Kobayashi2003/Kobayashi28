#include <iostream>
#include <vector>
#include <algorithm>

int main() {

    std::vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    if (auto itr = std::find(vec.begin(), vec.end(), 3); itr != vec.end()) * itr = 4; // init-statement in selection-statement only available with -std=c++17 or -std=gnu++17
    for (auto element : vec) std::cout << element << std::endl; // read only
    for (auto &element : vec) element += 1; // read and write
    for (auto element : vec) std::cout << element << std::endl; // read only

    return 0;
}