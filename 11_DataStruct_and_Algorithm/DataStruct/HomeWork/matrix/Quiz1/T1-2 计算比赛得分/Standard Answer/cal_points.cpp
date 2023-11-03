#include <iostream>
#include <vector>
#include <stack>
#include <sstream>
using namespace std;

int calPoints(vector<string>& ops);

int main() {
    vector<string> ops;
    int n;
    string op;

    cin >> n;
    for(int i = 0; i < n; ++i) {
        cin >> op;
        ops.push_back(op);
    }
    cout << calPoints(ops);
    return 0;
}

int calPoints(vector<string>& ops) {
    stack<int> scores;
    int ans = 0;

    for(auto& op: ops){
        if(op[0] == '+'){   // 计算上两次的得分总和
            int last = scores.top();
            scores.pop();
            int score = last + scores.top();
            scores.push(last);
            scores.push(score);
        } else if(op[0] == 'D') {
            scores.push(scores.top() * 2);
        } else if(op[0] == 'C') {
            scores.pop();
        } else { // 整数的情况
            scores.push(stoi(op));
        }
    }
    
    while(!scores.empty()){
        ans += scores.top();
        scores.pop();
    }
    return ans;
}