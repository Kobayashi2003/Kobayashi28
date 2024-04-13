#include<iostream>

using namespace std;

inline double square(double x) { return x * x; }

int main() {

    cout << square(1.1 + 2.3) << endl;
    return 0;
}
