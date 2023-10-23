#include <iostream>
#include <vector>

using namespace std;

class Solution {

private:

    const int des[8][2] = {{-1, 0}, {-1, 1}, {0, 1}, {1, 1},
                        {1, 0}, {1, -1}, {0, -1}, {-1, -1}};
    int temp = 0;
    vector<vector<int>> mark;

public:

    int MAX = 0;


public:

    Solution(int n, int m) {
        mark = vector<vector<int>>(n, vector<int>(m, 0));
    }

    void dfs(vector<vector<int>> matrix, int x, int y) {
        int n = matrix.size(), m = matrix[0].size();
        if (y == m) {
            dfs(matrix, x + 1, 0);
            return ;
        }
        if (x == n) {
            MAX = max(MAX, temp);
            return ;
        }

        dfs(matrix, x, y + 1); // do not choose

        if (!mark[x][y]) { // choose
            temp += matrix[x][y];
            for (int i = 0; i < 8; ++i) { // mark the 8 directions
                int nx = x + des[i][0], ny = y + des[i][1];
                if (nx >= 0 && nx < n && ny >= 0 && ny < m) {
                    mark[nx][ny] += 1;
                }
            }
            dfs(matrix, x, y + 1);
            for (int i = 0; i < 8; ++i) { // unmark the 8 directions
                int nx = x + des[i][0], ny = y + des[i][1];
                if (nx >= 0 && nx < n && ny >= 0 && ny < m) {
                    mark[nx][ny] -= 1;
                }
            }
            temp -= matrix[x][y];
        }
    }
};


int main() {

    int n, m; cin >> n >> m;

    vector<vector<int>> matrix(n, vector<int>(m, 0));

    for (int i = 0; i < n; ++i) {
        for (int j = 0 ; j < m; ++j) {
            cin >> matrix[i][j];
        }
    }

    Solution solution(n, m);

    solution.dfs(matrix, 0, 0);

    cout << solution.MAX << endl;

    return 0;
}