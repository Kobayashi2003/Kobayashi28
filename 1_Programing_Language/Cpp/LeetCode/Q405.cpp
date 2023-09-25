#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

class Solution {
public:
    string toHex(int num) {
        string hex = "";
        bool zf = true;
        for(short i = 0; i < 8; ++i) {
            unsigned num_tmp = (num & 0xF0000000) >> 28;
            char hex_ch = (num_tmp < 10 ? num_tmp+'0' : num_tmp-10+'a');
            if (hex_ch != '0' || (hex_ch == '0' && !zf)) {
                hex += hex_ch;
                zf = false;
            }
            num <<= 4;
        }
        return (hex == "" ? "0" : hex);
    }
};

int main() {

    int num; cin >> num;
    Solution s;
    cout << s.toHex(num) << endl;

    return 0;
}