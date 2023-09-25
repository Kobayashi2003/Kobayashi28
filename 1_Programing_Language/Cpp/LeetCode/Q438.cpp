#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        vector<int> ans;
        vector<unsigned> need = vector<unsigned>(26, 0);
        vector<unsigned> window = vector<unsigned>(26, 0);
        unsigned len_p = p.size();
        unsigned len_s = s.size();
        for (char c : p) 
            need[c - 'a']++;
        unsigned left = 0, right = 0;
        for (; right < len_s; ++right) {
            char c = s[right];
            if (need[c - 'a'] > 0) { // when c is in p 
                window[c - 'a']++;
                if (window[c - 'a'] > need[c - 'a']) { // when the number of c in window is more than that in p
                    for (; left < right; ++left) { // we need to find the first c in window then move the left of window to that position
                        if (s[left] == c) { 
                            left++;
                            break;
                        }
                        window[s[left] - 'a']--;
                    }
                    window[c - 'a']--;
                }   
            } else { // when c is not in p, we need to clear the window
                for (; left < right; ++left) {
                    window[s[left] - 'a']--;
                }
                left++;
            }
            if (right - left + 1 == len_p) {
                ans.push_back(left);
            }
        }
        return ans;
    }
};

int main() {
    Solution sol;
    string s = "cbaebabacd";
    string p = "abc";
    vector<int> ans = sol.findAnagrams(s, p);
    for (unsigned i = 0; i < ans.size(); i++) {
        cout << ans[i] << " ";
    }
    cout << endl;

    return 0;
}