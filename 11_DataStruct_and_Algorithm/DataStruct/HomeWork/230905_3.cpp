#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;


int solve(vector<int> a_horses, vector<int> b_horses) {
    int a_wins = 0, b_wins = 0;
    int n = a_horses.size();
    while (n) {
        if (a_horses[n-1] > b_horses[n-1]) {
            a_horses.pop_back();
            b_horses.pop_back();
            a_wins++;
        }
        else if (a_horses[n-1] < b_horses[n-1]) {
            a_horses.erase(a_horses.begin());
            b_horses.pop_back();
            b_wins++;
        }
        else {
            if (a_horses[0] > b_horses[0]) {
                a_horses.pop_back();
                b_horses.pop_back();
                a_wins++;
            }
            else {
                a_horses.erase(a_horses.begin());
                b_horses.pop_back();
                b_wins++;
            } 
        }
        n--;
    }
    if (a_wins > b_wins)
        return 1;
    else if (a_wins < b_wins) 
        return -1;
    else 
        return 0;
}


int main() {

    int n; cin >> n;
    vector<int> a_horses(n, 0), b_horses(n, 0);
    for (int i = 0; i < n; i++) 
        cin >> a_horses[i];
    for (int i = 0; i < n; i++)
        cin >> b_horses[i];

    sort(a_horses.begin(), a_horses.end());
    sort(b_horses.begin(), b_horses.end());

    // race a_horses with b_horses
    int a_won = solve(a_horses, b_horses);
    int b_won = solve(b_horses, a_horses);

    if (a_won == 0 || b_won == 0)
        cout << "YES" << endl;
    else if (!(n & 1) && a_won == 1 && b_won == 1)
        cout << "YES" << endl;
    else 
        cout << "NO" << endl;
  
    return 0;
}