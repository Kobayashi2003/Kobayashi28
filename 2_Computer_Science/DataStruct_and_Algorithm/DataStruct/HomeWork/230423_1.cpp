#include <iostream>
#include <vector>
#include <map>
#include <string>

using namespace std;
bool oneCharOff(string a, string b)
/*
函数名：oneCharOff
输入值：单词a，单词b
功  能：判断a，b是不是互为兄弟
*/
{
    if (a.size() != b.size()) // 判断两单词是否等长
        return false;
    else
    {
        int diff = 0;
        for (int i = 0; i < a.size(); ++i) {
            if (a[i] != b[i])
                if (++diff > 1) // 判断两单词是否只有一个字母不同
                    return false;
        } 
    }
    return true;
}

map<string, vector<string>> computeAdjacentWords(const vector<string> &words)
/*
函数名：computeAdjacentWords
输入值：单词列表 words
功  能：返回adjWords，其为键值对，键为单词，值为该单词所有的兄弟单词
*/
{
    map<string, vector<string>> adjWords;
    
    for (int i = 0; i < words.size(); ++i) {
        for (int j = i+1; j < words.size(); ++j) {
            if (oneCharOff(words[i], words[j])) {
                adjWords[words[i]].push_back(words[j]);
                adjWords[words[j]].push_back(words[i]);
            }
        }
    }

    return adjWords;
}

void printHighChangeables(const map<string, vector<string>> &adjWords, int minWords = 1)
/*
函数名：printHighChangeables
输入值：键值对 adjWords
功  能：打印所有兄弟单词判定结果
*/
{
    map<string, vector<string>>::const_iterator itr;
    for (itr = adjWords.begin(); itr != adjWords.end(); ++itr)
    {
        const pair<string, vector<string>> &entry = *itr;
        const vector<string> &words = entry.second;
        if (words.size() >= minWords)
        {
            cout << entry.first << ":" << words.size() << endl;
        }
    }
}
int main()
{
    int num;
    cin >> num;
    vector<string> a(num);
    for (int i = 0; i < num; i++)
    {
        cin >> a[i];
    }
    map<string, vector<string>> map;
    map = computeAdjacentWords(a);
    printHighChangeables(map);
    // system("pause");
    return 0;
}