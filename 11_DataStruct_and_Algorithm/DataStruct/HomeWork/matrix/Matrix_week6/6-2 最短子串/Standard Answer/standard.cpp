#include <iostream>
#include <string>
using namespace std;
string minWindow(string S, string T) {
        if (S.empty() || T.empty())
        {
            return "No";
        }
        int count = T.size();
        int require[128] = {0};
        bool chSet[128] = {false};
        for (int i = 0; i < count; ++i)
        {
            require[T[i]]++;
            chSet[T[i]] = true;
        }
        int i = -1;
        int j = 0;
        int minLen = 999999999;
        int minIdx = 0;
        while (i < (int)S.size() && j < (int)S.size())
        {
            if (count)
            {
                i++;
                require[S[i]]--;
                if (chSet[S[i]] && require[S[i]] >= 0)
                {
                    count--;
                }
            }
            else
            {
                if (minLen > i - j + 1)
                {
                    minLen = i - j + 1;
                    minIdx = j;
                }
                require[S[j]]++;
                if (chSet[S[j]] && require[S[j]] > 0)
                {
                    count++;
                }
                j++;
            }
        }
        if (minLen == 999999999)
        {
            return "No";
        }
        return S.substr(minIdx, minLen);
    }

int main()
{
    string s, t;
    cin >> s >> t;
    cout << minWindow(s,t);
    return 0;
}