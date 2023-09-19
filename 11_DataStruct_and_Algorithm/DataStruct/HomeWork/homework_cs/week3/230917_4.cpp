#include <iostream>
#include <stack>
#include <vector>

using namespace std;

using ll = long long;


class Solution {

    int n, m;

public:
    Solution(int n, int m) : n(n), m(m) {}

    ll Ackerman(int n, int m) {
        if (n == 0) return 1;
        if (m == 0) {
            if (n == 1) return 2;
            else return n + 2;
        }
        return Ackerman(Ackerman(n - 1, m), m - 1);
    }

    ll Ackerman_non_recursive(int n, int m) {
        stack<vector<ll>> s; // simulate the recursive stack
        s.push({n, m, 0}); 
        stack<ll> res; // simulate the recursive return value

        while (!s.empty()) {
            auto v = s.top(); s.pop();
            int n_cur = v[0], m_cur = v[1], state = v[2];

            // the condition of the end of the loop
            if (n_cur == 0) {
                res.push(1);
                continue;
            } else if (m_cur == 0) {
                if (n_cur == 1) res.push(2);
                else res.push(n_cur + 2);
                continue;
            }            

            // change the recursive operation to stack operation
            if (state == 0) {
                s.push({n_cur, m_cur, 1});
                s.push({n_cur - 1, m_cur, 0});
            } else if (state == 1) {
                s.push({res.top(), m_cur - 1, 0});
                res.pop();
            } 
        }

        return res.top();
    }

};

int main() {

    int n, m; cin >> n >> m;
    Solution s(n, m);
    cout << s.Ackerman(n, m) << endl;
    cout << s.Ackerman_non_recursive(n, m) << endl;

    return 0;
}