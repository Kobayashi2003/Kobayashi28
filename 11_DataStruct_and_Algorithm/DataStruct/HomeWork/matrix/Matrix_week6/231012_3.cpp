#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Solution {

public:

    Solution() { }

    int maxWin(string str1, string str2) {

        int maxLen = 0;
        int len1 = str1.length(), len2 = str2.length();

        vector<vector<int>> dp(len1+1, vector<int>(len2+1, 0));

        for (int i = 1; i <= len1; ++i) {
            for (int j = 1; j <= len2; ++j) {
                if (str1[i-1] == str2[j-1])
                    dp[i][j] = dp[i-1][j-1] + 1;
                else
                    dp[i][j] = 0;
                if (dp[i][j] > maxLen)
                    maxLen = dp[i][j];
            }
        }

        return maxLen;
    }

};


int main() {

    Solution sol;
    // string str1 = "helloworld";
    // string str2 = "loop";
    string str1, str2;
    cin >> str1 >> str2;
    cout << sol.maxWin(str1, str2) << endl;

    return 0; 
}