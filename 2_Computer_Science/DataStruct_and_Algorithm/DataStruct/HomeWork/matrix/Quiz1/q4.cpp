#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;


void simulate(vector<int> &simu) {
    vector<int> result;
    while (!simu.empty()) {
        result.push_back(simu.front());
        simu.erase(simu.begin());
        if (!simu.empty()) {
            simu.push_back(simu.front());
            simu.erase(simu.begin());
        }
    }

    simu = result;
}


int main() {

    int n; cin >> n;
    vector<int> cards(n);

    for (int i = 0; i < n; ++i) 
        cin >> cards[i];
    sort(cards.begin(), cards.end());

    vector<int> simu(n);
    for (int i = 0; i < n; ++i) 
        simu[i] = i;
    simulate(simu);

    vector<int> result(n);
    for (int i = 0; i < n; ++i) {
        result[simu[i]] = cards[i];
    }

    for (int i = 0; i < n; ++i) 
        if (i != n - 1)
            cout << result[i] << ",";
        else 
            cout << result[i] << endl;

    return 0;
}