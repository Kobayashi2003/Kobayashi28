// ref: http://www.ruanyifeng.com/blog/2013/05/boyer-moore_string_search_algorithm.html
// ref: https://blog.csdn.net/aruewds/article/details/115254348
#include <iostream>
#include <string>
#include <map>
#include <vector>

using namespace std;

class myString : public string {

public:

    myString() : string() {}
    myString(const string & s) : string(s) {}
    myString(const char * s) : string(s) {}

    int GetIndex(const string & pat) {
        return this->GetIndex(pat, 0);
    }

    int GetIndex(const string & pat, unsigned int start) {
        string sub = this->substr(start);
        return this->BM(sub, pat);
    }

private:

    void GetBadCharTable(const string & pat, map<char, int> & table) {
        int pLen = pat.size();
        for (int i = 0; i < pLen; i++) {
            table[pat[i]] = i;
        }
    }


   void GetGoodSuffixTable(const string & pat, vector<int> & suffix, vector<bool> & prefix) {
        int pLen = pat.size();
        for (int i = 0; i < pLen; i++) {
            suffix[i] = -1;
            prefix[i] = false;
        }
        for (int i = 0; i < pLen - 1; i++) {
            int j = i;
            int k = 0;
            while (j >= 0 && pat[j] == pat[pLen-1-k]) {
                j--;
                k++;
                suffix[k] = j + 1; // if k == 1, the suffix[k] is the value of
                                    // the matching position corresponding to a character length suffix
            }
            if (j == -1) {
                prefix[k] = true;  // means that matching suffix is a prefix of the pattern
            }
        }
    }


    int getGsMove(const vector<int> & suffix, const vector<bool> & prefix, int index, int sLen) {
        // index is the index of the first character of the mismatched suffix (bad character)
        // len is the length of the good suffix
        int pLen = suffix.size();
        int len = sLen - index - 1;
        if (suffix[len] != -1) {
            return index + 1 - suffix[len]; // the move distance = 
                                           // the position of the good suffix - suffix[len]
        }
        for (int i = index + 2; i < sLen; i++) {
            if (prefix[sLen - i]) {
                return i;
            }
        }
        return pLen;
    }


    int BM(const string & s, const string & pat) {
        int sLen = s.size(), pLen = pat.size();
        if (sLen < pLen) return -1;

        // generate bad character rule table
        map<char, int> badCharTable;
        GetBadCharTable(pat, badCharTable);

        // generate good suffix rule table
        vector<int> suffix(pLen, -1);
        vector<bool> prefix(pLen, false);
        GetGoodSuffixTable(pat, suffix, prefix);

        // search
        int i = 0;
        while (i <= sLen - pLen) {
            int j = pLen - 1;
            while (j >= 0 && s[i+j] == pat[j]) { // matching from right to left
                j--;
            }
            if (j < 0) { // matching successfully
                return i;
            }
            else {
                int badCharMove = j - badCharTable[s[i+j]];
                int goodSuffixMove = 0;
                if (j < pLen - 1) {
                    goodSuffixMove = getGsMove(suffix, prefix, j, sLen);
                }
                i += max(badCharMove, goodSuffixMove);
            }
        }

        return -1;
    }
};


int main() {

    myString s = "ababababca";
    string p = "banana";

    cout << s.GetIndex(p) << endl;

    return 0;
}