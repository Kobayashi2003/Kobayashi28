#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;

vector<string> findRepeatedDnaSequences(string s)
/*
函数名：findRepeatedDnaSequences
输入值：DNA序列s
功  能：查找重复的DNA序列并保存在result中
*/
{
    vector<string> result;
    map<string, int> count_map;
    for (int i = 0; i < (int)s.size() - 9; ++i) {
        string sub = s.substr(i, 10);
        if (count_map.find(sub) == count_map.end()) {
            count_map[sub] = 1;
        } else {
            count_map[sub]++;
            result.push_back(sub);
        }
    }
    return result;
}

void printResult(vector<string> &result)
{
    for (int i = 0; i < (int)result.size(); i++)
    {
        cout << result[i] << endl;
    }
}

int main()
{
    string s;
    cin >> s;
    vector<string> result = findRepeatedDnaSequences(s);
    printResult(result);
    return 0;
}