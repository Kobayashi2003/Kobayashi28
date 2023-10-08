#include <iostream>
#include <string>
#include <stack>

using namespace std;

string removeKdigits(string num, int k);

string removeKdigits(string num, int k) {

    stack<char> s;
    int len = num.size();
    if (len == k) return "0";

    for (int i = 0; i < len; i++) {
        while (!s.empty() && k > 0 && s.top() > num[i]) {
            s.pop();
            k--;
        }
        s.push(num[i]);
    }

    while (k > 0) {
        s.pop();
        k--;
    }

    string res = "";
    while (!s.empty()) {
        res = s.top() + res;
        s.pop();
    }

    while (res[0] == '0') res.erase(res.begin());

    return res == "" ? "0" : res;
}