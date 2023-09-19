#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    int t;
    int n;
    int a;
    queue<int> q;
    cin >> t;
    while (t--) {
        cin >> n;
        for (int i = 1; i <= n; i++)
            q.push(i);
        while (q.size() > 1) {
            cout << q.front() << ' ';
            q.pop();
            a = q.front();
            q.pop();
            q.push(a);
        }
        cout << q.front() << ' ' << endl;
        q.pop();
    }
    return 0;
}