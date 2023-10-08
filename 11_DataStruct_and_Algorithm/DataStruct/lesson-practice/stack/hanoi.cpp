#include <iostream>

class Solution {

public:

    void hanoi(int n) {
        return hanoi(n, 'A', 'B', 'C');
    }

    void hanoi(int n, char from, char to, char aux) {
        if (n == 1) {
            std::cout << "Move disk 1 from " << from << " to " << to << std::endl;
            return;
        }
        hanoi(n-1, from, aux, to);
        std::cout << "Move disk " << n << " from " << from << " to " << to << std::endl;
        hanoi(n-1, aux, to, from);
    }

};

int main() {

    Solution s;
    s.hanoi(3);

    return 0;
}