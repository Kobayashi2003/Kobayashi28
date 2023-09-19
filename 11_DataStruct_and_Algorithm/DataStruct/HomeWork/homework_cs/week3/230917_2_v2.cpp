#include <iostream>
#include <vector>

using namespace std;


void upstairs(int total) {
    vector<vector<vector<int>>> dp(total+1);
    dp[1].push_back({1});
    dp[2].push_back({1, 1}); dp[2].push_back({2});
    for (int i = 3; i <= total; ++i) {
        for (size_t j = 0; j < dp[i-1].size(); ++j) {
            vector<int> tmp = dp[i-1][j];
            tmp.push_back(1);
            dp[i].push_back(tmp);
        }
        for (size_t j = 0; j < dp[i-2].size(); ++j) {
            vector<int> tmp = dp[i-2][j];
            tmp.push_back(2);
            dp[i].push_back(tmp);
        }
    }
    for (size_t i = 0; i < dp[total].size(); ++i) {
        for (size_t j = 0; j < dp[total][i].size(); ++j) {
            cout << dp[total][i][j] << " ";
        }
        cout << endl;
    }
}


int main() {

    int total; cin >> total;
    upstairs(total);
    
    return 0;
}