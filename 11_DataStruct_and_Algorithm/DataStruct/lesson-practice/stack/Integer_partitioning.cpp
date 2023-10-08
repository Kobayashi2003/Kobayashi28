#include <iostream>

// positive integer partitioning
/*
q(n, m) =  {

    1,                       if n = 1 or m = 1
    q(n, n),                 if n < m
    1 + q(n, n-1),           if n = m
    q(n, m-1) + q(n-m, m),   n > m > 1
}
*/

class Solution {

public:

    int partition(int n) {
        return partition(n, n);
    }

    int partition(int n, int m) {
        if (n == 1 || m == 1) return 1;
        if (n < m) return partition(n, n);
        if (n == m) return 1 + partition(n, n-1);
        return partition(n, m-1) + partition(n-m, m);
    }

};

int main() {

    Solution s;
    std::cout << s.partition(6) << std::endl;

    return 0;
}