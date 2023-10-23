#include <iostream>
#include <stack>
#include <vector>

using namespace std;

int rain(vector<int> &height) {
    int ans = 0, current = 0;

    stack<int> st;

    while (current < height.size()) {
        while (!st.empty() && height[current] > height[st.top()]) {
            int top = st.top();
            st.pop();

            if (st.empty()) {
                break;
            }

            int distance = current - st.top() - 1;
            int bounded_height = min(height[current], height[st.top()]) - height[top];

            ans += distance * bounded_height;
        }

        st.push(current++);
    }

    return ans;
}

int main() {

    int N; cin >> N;

    vector<int> height(N);

    for (int i = 0; i < N; i++) {
        cin >> height[i];
    }

    cout << rain(height) << endl;

    return 0;
}