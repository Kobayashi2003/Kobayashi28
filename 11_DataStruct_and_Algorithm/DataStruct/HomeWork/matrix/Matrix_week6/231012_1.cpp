#include <iostream>
#include <string>

using namespace std;

class Solution {

public:
    Solution() { }
    
    int longestSubStr(string str) {
        int maxLen = 0;
        int len = str.length();

        if (len <= 1) return len;

        int left = 0, right = 1;

        int lastAppear[256];
        for (int i = 0; i < 256; i++) {
            lastAppear[i] = -1;
        }

        int curLen = 1;
        lastAppear[int(str[left])] = left;

        while (right < len) {
            if (lastAppear[int(str[right])] >= left) {
                left = lastAppear[int(str[right])] + 1;
                lastAppear[int(str[right])] = right;
                right++;
                curLen = right - left;
            } else {
                lastAppear[int(str[right])] = right;
                right++;
                curLen++;
            }
            if (curLen > maxLen) maxLen = curLen;
        }

        return maxLen;
    }
};

int main() {

    Solution sol;
    string str; cin >> str;
    cout << sol.longestSubStr(str) << endl;

    return 0;
}