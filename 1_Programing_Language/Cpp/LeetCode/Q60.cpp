#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    vector<double> dicesProbability(int n) {
        vector<double> res(6, 1.0 / 6.0);
        for (int i = 2; i <= n; ++i) {
            vector<double> tmp(5 * i + 1, 0);
            for (int j = 0; j < res.size(); ++j) {
                for (int k = 0; k < 6; ++k) {
                    tmp[j + k] += res[j] / 6.0;
                }
            }
            res = tmp;
        }
        return res;
    }


    vector<double> dicesProbability_2(int n) {
        // dp[i][j] : i is the number of dices, 
        // j is the sum of the dices
        // and dp[i][j] is the number of the sum j
        vector<vector<int>> dp(n + 1, vector<int>(6 * n + 1, 0));
        for (int i = 1; i <= 6; ++i) {
            dp[1][i] = 1;
        }
        for (int i = 2; i <= n; ++i) {
            for (int j = i; j < 6 * i + 1; ++j) {
                for (int k = 1; k <= 6; ++k) {
                    if (j - k <= 0) {
                        break;
                    }
                    dp[i][j] += dp[i - 1][j - k];
                }
            }
        }
        vector<double> res;
        for (int i = n; i < 6 * n + 1; ++i) {
            res.push_back(dp[n][i] * 1.0 / pow(6, n));
        }
        return res;
    }

    
    vector<double> dicesProbability_3(int n) {
        vector<double> dp(6*n+1, 0);
        for (int i = 1; i <= 6; ++i) dp[i] = 1.0;
        for (int i = 2; i <= n; ++i) {
            for (int j = 6 * i; j >= i; --j) {
                dp[j] = 0;
                for (int k = 1; k <= 6; ++k) {
                    if (j - k < i - 1) {
                        break;
                    }
                    dp[j] += dp[j - k];
                }
            }
        }
        for (int i = 0; i < dp.size(); ++i) {
            dp[i] /= pow(6, n);
        }
        return vector<double>(dp.begin() + n, dp.end());
    }
};