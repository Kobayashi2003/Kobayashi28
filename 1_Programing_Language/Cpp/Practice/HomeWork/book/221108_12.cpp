#include <iostream>

using namespace std;

template <typename numtype>
class Compare {
public:
    Compare(numtype a, numtype b) : x(a), y(b) {}
    numtype max();
    numtype min();
private:
    numtype x, y;
};

template <typename numtype>
numtype Compare<numtype>::max() {
    return x > y ? x : y;
}

template <typename numtype>
numtype Compare<numtype>::min() {
    return x < y ? x : y;
}

int main() {
    Compare<int> cmp1(3, 7);
    cout << cmp1.max() << " is the Maxium of two integers." << endl;
    cout << cmp1.min() << " is the Minium of two integers." << endl;

    Compare<float> cmp2(45.78, 93.6);
    cout << cmp2.max() << " is the Maxium of two floats." << endl;
    cout << cmp2.min() << " is the Minium of two floats." << endl;

    Compare<char> cmp3('a', 'A');
    cout << cmp3.max() << " is the Maxium of two chars." << endl;
    cout << cmp3.min() << " is the Minium of two chars." << endl;

    return 0;
}