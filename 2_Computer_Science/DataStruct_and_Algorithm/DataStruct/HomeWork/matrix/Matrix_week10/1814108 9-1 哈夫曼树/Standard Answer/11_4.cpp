#include <iostream>
#include <queue>
using namespace std;

priority_queue<int, vector<int>, greater<int>> mq;


int main() {
    int n;
    cin >> n;
    int tmp;
    for (int i = 0; i < n; i++) {
        cin >> tmp;
        mq.push(tmp);
    }
    int sum = 0;
    int a, b;
    while (mq.size() > 1) {
        a = mq.top();
        mq.pop();
        b = mq.top();
        mq.pop();
        sum += a+b;
        mq.push(a+b);
    }
    cout << sum << endl;
}