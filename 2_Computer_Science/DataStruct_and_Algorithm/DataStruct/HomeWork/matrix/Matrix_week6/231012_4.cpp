#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Solution {
public:
    string longestPalindrome(string s) {
        int len = s.length();

        if (len < 2) return s;

        // dp[i][j] = true means s[i...j] is a palindrome
        vector<vector<bool>> dp(len, vector<bool>(len, false));

        int maxLen = 1;
        int start = 0;

        for (int i = 0; i < len; ++i) { // every char is a palindrome
            dp[i][i] = true;
        }


        /*
        *  P(i, i)   = true
        *  P(i, i+1) = (Si == Si+1)
        *  P(i, j)   = P(i+1, j-1) && (Si == Sj)
        */

        for (int j = 1; j < len; ++j) {
            for (int i = 0; i < j; ++i) {
                if (s[i] == s[j]) {
                    if (j - i < 3) { // j - i == 1 or 2
                        dp[i][j] = true;
                    } else {
                        dp[i][j] = dp[i+1][j-1];
                    }
                } else {
                    dp[i][j] = false;
                }

                if (dp[i][j]) {
                    int curLen = j - i + 1;
                    if (curLen > maxLen) {
                        maxLen = curLen;
                        start = i;
                    }
                }
            }
        }
        
        return s.substr(start, maxLen);
    }
};

int main() {
    Solution sol;
    string str; cin >> str;
    cout << sol.longestPalindrome(str) << endl;

    return 0;
}