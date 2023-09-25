#include <iostream>
#include <string>
#include <cstring>

using namespace std;

class Solution {

    string s;

public:
    Solution(string s) { this->s = s; }

    int lenthOfLongsetSubstring(string s) {
        int maxLen = 0;
        int begin = 0, end = 0;
        short charMap[256];
        memset(charMap, -1, sizeof(charMap));
        for (int i = 0; i < s.size(); ++i) {
            if (charMap[short(s[i])] != -1 && charMap[short(s[i])] >= begin) {
                begin = charMap[short(s[i])] + 1;
            }
            charMap[short(s[i])] = i;
            end = i;
            if (end - begin + 1 > maxLen) {
                maxLen = end - begin + 1;
            }
        }
        return maxLen;
    }
};


int main() {
    string s = " ";
    Solution solution(s);
    cout << solution.lenthOfLongsetSubstring(s) << endl;

    return 0;
}