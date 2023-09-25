#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> combination(vector<int> &nums) {
    if (nums.empty()) return {};
    if (nums.size() == 1) return {nums};

    vector<vector<int>> res;
    for (int i = 0; i < nums.size(); i++) {
        int tmp = nums[0];
        nums[0] = nums[i];
        nums[i] = tmp;
        vector<int> sub = vector<int>(nums.begin() + 1, nums.end());
        vector<vector<int>> sub_res = combination(sub);
        for (auto &v : sub_res) {
            v.insert(v.begin(), nums[0]);
            res.push_back(v);
        }
    }
    return res;
}

int main() {

    vector<int> nums = {1, 2, 3, 4};
    vector<vector<int>> res = combination(nums);
    for (auto &v : res) {
        for (auto &i : v) {
            cout << i << " ";
        }
        cout << endl;
    }

    return 0;
    
}