#include <iostream>

using namespace std;

int main() {

    int nums[10] = {0,};
    for (int i = 0; i < 10; ++i) 
        cin >> nums[i];
    int target; cin >> target;

    int i1, i2;
    for (i1 = 0; i1 < 10; ++i1) {
        for (i2 = i1+1; i2 < 10; ++i2) {
            if (nums[i1] + nums[i2] == target) {
                cout << i1 << " " << i2 << endl;
                return 0;
            }
        }
    }

    return 0;
}