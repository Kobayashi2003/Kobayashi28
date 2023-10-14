#include <iostream>
#include <string>

using namespace std;

// const int INT_MAX = 2147483647;

class Solution {

public:
    Solution() { }
    
    string minWindow(string str, string T) {
        string res = "";

        int len = str.length();

        if (len < T.length()) return "";

        int hash[52] = {0,};
        auto hashFunc = [&](char c) { return c >= 'a' ? c - 'a' : c - 'A' + 26; };
        for (auto ch : T) 
            hash[hashFunc(ch)]++;

        int minLen = INT_MAX;
        int left_record = 0;

        int left = 0, right = 0;
        int rest2find = T.length();

        int charCount[52] = {0,};

        while (right < len) {

            if (hash[hashFunc(str[right])] > 0) {
                charCount[hashFunc(str[right])]++;
                if (charCount[hashFunc(str[right])] <= hash[hashFunc(str[right])])
                    rest2find--;
            }

            while (!rest2find) {
                if (hash[hashFunc(str[left])] > 0) {
                    charCount[hashFunc(str[left])]--;
                    if (charCount[hashFunc(str[left])] < hash[hashFunc(str[left])])
                        rest2find++;
                }
                if (rest2find && right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    left_record = left;
                }
                left++;
            }

            right++;
        }

        if (minLen == INT_MAX) return "";
        return str.substr(left_record, minLen);
    }
};

int main() {

    Solution sol;
    string str; cin >> str;
    string T; cin >> T;

    cout << sol.minWindow(str, T) << endl;

    return 0;
}