#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int main() {

    int n; cin >> n;

    vector<char> ch(n);
    vector<int> weight(n);
    vector<string> value(n, "");

    for (int i = 0; i < n; ++i) {
        cin >> ch[i] >> weight[i];
        value[i] += ch[i];
    }

    for (int i = 0; i < n-1; ++i) {
        int min1 = 1e9, min2 = 1e9;
        int min1_index = -1, min2_index = -1;
        for (int j = 0; j < n-i; ++j) {
            if (weight[j] < min1 && weight[j] != 0) {
                min2 = min1;
                min2_index = min1_index;
                min1 = weight[j];
                min1_index = j;
            } else if (weight[j] < min2 && weight[j] != 0) {
                min2 = weight[j];
                min2_index = j;
            }
        }
        if (min1 == min2) {
            if (ch[min1_index] < ch[min2_index])
                swap(min1_index, min2_index);
        } else { // min1 < min2
            swap(min1_index, min2_index);
        }

        ch.push_back('#');        
        ch.erase(ch.begin() + min1_index);
        ch.erase(ch.begin() + min2_index - (min2_index > min1_index ? 1 : 0));

        int weight_new  = weight[min1_index] + weight[min2_index];
        weight.push_back(weight_new);
        weight.erase(weight.begin() + min1_index);
        weight.erase(weight.begin() + min2_index - (min2_index > min1_index ? 1 : 0));

        string value_new = value[min1_index] + value[min2_index];
        value.push_back(value_new);
        value.erase(value.begin() + min1_index);
        value.erase(value.begin() + min2_index - (min2_index > min1_index ? 1 : 0));
    }

    for (char ch : value[0]) {
        cout << ch << endl;
    }

    return 0;
}