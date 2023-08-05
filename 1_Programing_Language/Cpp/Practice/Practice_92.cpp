// calculate right shift

// if i_num is positive:
// i_num >> shift_num, and fill 0 to left

// if i_num is negative:
// (i_num + bias) >> shift_num, and fill 1 to left
// bias = 2^shift_num - 1

#include <iostream>

using namespace std;

void show_bit(unsigned int num) {
    bool bit[32] = {0,};
    unsigned tmp_num = num;
    for (int i = 0; i < 32; ++i) {
        bit[i] = tmp_num & 1;
        tmp_num >>= 1;
    }
    for (int i = 31; i >= 16; --i) {
        cout << bit[i];
    }
    cout << endl;
    for (int i = 15; i >= 0; --i) {
        cout << bit[i];
    }
    cout << endl;
}

int main() {

    union {
        int i_num;
        unsigned int u_num;
    } num;
    cin >> num.i_num;

    show_bit(num.u_num);

    unsigned short shift_num; cin >> shift_num;

    num.u_num = (num.i_num == 0) ? 0 :
        (num.i_num < 0 ? 
            (num.u_num + (1 << shift_num) - 1) >> shift_num | ~0 << (32 - shift_num) :
            (num.u_num >> shift_num)
        );

    show_bit(num.u_num);
    cout << num.i_num << endl;

    return 0;   
}