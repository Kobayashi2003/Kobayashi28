#include <iostream>
#include <string>
#include <vector>

using namespace std;

// const int INT_MAX = 2147483647;

class Solution {

public:
    Solution() { }
    
    string minWindow(string str, string T) {
        string res = "";
        int minLen = INT_MAX;

        int len = str.length();
        if (len < T.length()) return "No";
        if (len == 1) return str == T ? str : "No";
        if (T.length() == 1) return str.find(T) != string::npos ? T : "No";

        int char_in_T[26] = {0,}; // A-Z
        for (int i = 0; i < T.length(); i++)
            char_in_T[int(T[i]) - 65]++;
        int charCount[26] = {0,};
        vector<vector<int>> charAppear;
        for (int i = 0; i < 26; i++) {
            vector<int> tmp; charAppear.push_back(tmp);
        }

        int rest2find = T.length();
        int left = 0, right = 0;
        int left_record = 0;

        auto inT = [&](char c) { return char_in_T[int(c) - 65]; };

        while (right < len) {

            while (!inT(str[left]))
                left++;
            if (!(left < len-1)) break;
            if (left >= right) {
                right = left + 1;
                charCount[int(str[left]) - 65]++;
                charAppear[int(str[left]) - 65].push_back(left);
                rest2find--;
            }

            if (inT(str[right])) {
                
                if (!rest2find) {
                    int new_left = charAppear[int(str[right]) - 65][
                        charCount[int(str[right]) - 65] - char_in_T[int(str[right]) - 65]
                    ];
                    while (left <= new_left) {
                        if (inT(str[left])) {
                            charAppear[int(str[left]) - 65].erase(charAppear[int(str[left]) - 65].begin());
                            if (charCount[int(str[left]) - 65] <= char_in_T[int(str[left]) - 65])
                                rest2find++;
                            charCount[int(str[left]) - 65]--;
                        }
                        left++;
                    }
                }

                charCount[int(str[right]) - 65]++;
                charAppear[int(str[right]) - 65].push_back(right);
                if (charCount[int(str[right]) - 65] <= char_in_T[int(str[right]) - 65]) {
                    rest2find--;
                }

                while (true) {
                    if (!inT(str[left])) left++;
                    else {
                        if (charCount[int(str[left]) - 65] <= char_in_T[int(str[left]) - 65]) break;
                        else {
                            charAppear[int(str[left]) - 65].erase(charAppear[int(str[left]) - 65].begin());
                            charCount[int(str[left]) - 65]--;
                        }
                        left++;
                    }
                }
            }

            if (!rest2find && right - left < minLen) {
                minLen = right - left;
                left_record = left;
            }

            right++;
        }

        if (minLen != INT_MAX) {
            res = str.substr(left_record, minLen + 1);
        }

        return res == "" ? "No" : res;
    }
};

int main() {

    Solution sol;
    string str; cin >> str;
    string T; cin >> T;

    cout << sol.minWindow(str, T) << endl;

    return 0;
}