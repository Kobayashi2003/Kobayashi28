#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    bool checkPossibility(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n - 1; ++i) {
            int x = nums[i], y = nums[i + 1];
            if (x > y) {
                nums[i] = y;
                if (is_sorted(nums.begin(), nums.end())) {
                    return true;
                }
                nums[i] = x;
                nums[i + 1] = x;
                return is_sorted(nums.begin(), nums.end());
            }
        }
        return true;
    }

    bool checkPossibility1(vector<int> & nums) {
        int n = nums.size(), cnt = 0;
        for (int i = 0; i < n - 1; ++i) {
            int x = nums[i], y = nums[i + 1];
            if (x > y) {
                cnt++;
                if (cnt > 1)
                    return false;

                if (i > 0 && y < nums[i - 1])
                    // think about 2 case:
                    // 4 [7] 5 6
                    // 4 7 [3] 9
                    nums[i + 1] = x;
            }
        }
    }
};