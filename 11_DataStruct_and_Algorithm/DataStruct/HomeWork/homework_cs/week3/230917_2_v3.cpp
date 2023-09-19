#include <iostream>
#include <vector>

using namespace std;

class Solution {

    int total;
    vector<vector<int>> res;

public:
    Solution(int total) : total(total) {}

    vector<vector<int>> upstairs() {
        vector<int> path;
        int rest = total;
        path.push_back(1); rest -= 1;
        upstairs(rest, path);
        path.pop_back(); rest += 1;
        path.push_back(2); rest -= 2;
        upstairs(rest, path); 
        return res;
    }

    void upstairs(int rest, vector<int> path) {
        if (rest < 0) return;
        else if (rest == 0) res.push_back(path);
        else {
            path.push_back(1); rest -= 1;
            upstairs(rest, path);
            path.pop_back(); rest += 1;
            path.push_back(2); rest -= 2;
            upstairs(rest, path);
        }
    }
};


int main() {

    Solution path(5);
    vector<vector<int>> res = path.upstairs();
    for (auto & v : res) {
        for (auto & i : v) {
            cout << i << " ";
        }
        cout << endl;
    }
    return 0;
}