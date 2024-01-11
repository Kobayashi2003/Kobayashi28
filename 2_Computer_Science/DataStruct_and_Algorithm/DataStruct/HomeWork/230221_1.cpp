#include <iostream>

using namespace std;

const float PI = 3.14159;
const float Price_1 = 20;
const float Price_2 = 35;


int main() {

    float r = 0; cin >> r;

    float fence_price = Price_1 * 2 * PI * r;
    float cement_price = Price_2 * (PI * (r+3)*(r+3) - PI * r * r);

    cout << fence_price << endl;
    cout << cement_price << endl;

    return 0;
}