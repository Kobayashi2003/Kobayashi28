#include <iostream>
#include "ch6_34.hpp"

using namespace std;

int main() {
    // 12 21 24 65 14 26 16 18 23 51 24 65 13
    BiQueue<int> bq;
    bq.insert(12);
    bq.insert(21);
    bq.insert(24);
    bq.insert(65);
    bq.insert(14);
    bq.insert(26);
    bq.insert(16);
    bq.insert(18);
    bq.insert(23);
    bq.insert(51);
    bq.insert(24);
    bq.insert(65);
    bq.insert(13);

    return 0;
}