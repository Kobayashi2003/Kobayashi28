#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

vector<int> deckRevealedIncreasing(vector<int>& deck);
void printAns(vector<int>& ans);

int main() {
    vector<int> deck;
    int n, num;
    cin >> n;
    for(int i = 0; i < n; ++i) {
        cin >> num;
        deck.push_back(num);
    }

    vector<int> ans = deckRevealedIncreasing(deck);
    printAns(ans);
    return 0;
}

vector<int> deckRevealedIncreasing(vector<int>& deck) {
    // 在队列中存入答案数组的下标值，通过模拟可以知道依次进行输出的下标的顺序
    sort(deck.begin(),deck.end());
    vector<int> ans(deck.size(),0);
    queue<int> q;
    for(int i=0;i<deck.size();++i){
        q.push(i);
    }
    int cur=0;
    while(!q.empty()){
        int index=q.front();
        ans[index]=deck[cur++];
        q.pop();
        q.push(q.front());
        q.pop();
    }
    return ans;
}

void printAns(vector<int>& ans) {
    cout << ans[0];
    for(int i = 1; i < ans.size(); ++i) {
        cout << "," << ans[i];
    }
}