#include <iostream>
#include <vector>

using namespace std;

int removeDuplicates(vector<int>& nums) {
    int len = nums.size();
    if (len == 0) return 0;
    int i = 0;
    for (int j = 1; j < len; j++) {
        if (nums[j] != nums[i]) {
            i++;
            nums[i] = nums[j];
        }
    }
    return i+1;
}

int main() {

    vector<int> v;
    int num;
    while (cin >> num) {
        v.push_back(num);
    }
    cout << removeDuplicates(v) << endl;
    return 0;
}