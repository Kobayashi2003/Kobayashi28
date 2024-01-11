#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {

    int n; cin >> n;
    vector<string> ops(n);

    for (int i = 0; i < n; ++i) 
        cin >> ops[i];

    vector<int> record;

    for (string op : ops) {
        if (op == "C") 
            record.pop_back();
        else if (op == "D")
            record.push_back(record[record.size() - 1] * 2);
        else if (op == "+")
            record.push_back(record[record.size() - 2] + record[record.size() - 1]);
        else 
            record.push_back(stoi(op));
    }

    int sum = 0;
    for (int num : record) 
        sum += num;

    cout << sum << endl;

    return 0;
}