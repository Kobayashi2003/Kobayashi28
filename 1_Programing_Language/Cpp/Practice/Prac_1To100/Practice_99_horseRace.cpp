// 田忌赛马
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {

    int horse_num; cin >> horse_num;
    vector<int> a_horses, b_horses;
    for (int i = 0; i < horse_num; i++) {
        int horse; cin >> horse;
        a_horses.push_back(horse);
    }
    for (int i = 0; i < horse_num; i++) {
        int horse; cin >> horse;
        b_horses.push_back(horse);
    }

    sort(a_horses.begin(), a_horses.end());
    sort(b_horses.begin(), b_horses.end());

    int a_wins = 0, b_wins = 0;
    int result = 0; // 1: a win; -1: b win; 0: draw

    for (int i = 0; i < horse_num; i++) {

        int fastest_a = a_horses.back(),
            fastest_b = b_horses.back(),
            slowest_a = a_horses.front(),
            slowest_b = b_horses.front();

        if (fastest_a > fastest_b) {
            a_wins++;
            a_horses.pop_back();
            b_horses.pop_back();
        } else if (fastest_a < fastest_b) {
            b_horses.pop_back();
            a_horses.erase(a_horses.begin());
            b_wins++;
        } else {
            if (slowest_a > slowest_b) {
                a_wins++;
                a_horses.pop_back();
                b_horses.pop_back();
            } else if (slowest_a < slowest_b) {
                b_horses.pop_back();
                a_horses.erase(a_horses.begin());
                b_wins++;
            }
        }
    }

    result = (a_wins > b_wins) - (a_wins < b_wins);
    cout << result << endl;

    return 0;
}