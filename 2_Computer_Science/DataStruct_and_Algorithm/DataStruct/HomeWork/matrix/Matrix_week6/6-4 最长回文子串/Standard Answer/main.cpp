#include<iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
string longestPalindrome(string s) {
	if (s.empty()) {
		return s;
	}
	string s_rev = s;
	reverse(s_rev.begin(), s_rev.end());
	int len = s.length();
	vector<vector<int> > arr;
	vector<int> temp;
	for (int i = 0; i < len; i++) {
		temp.push_back(0);
	}
	for (int i = 0; i < len; i++) {
		arr.push_back(temp);
	}
	int maxLen = 0;
	int maxEnd = 0;
	for (int i = 0; i < len; i++) {
		for (int j = 0; j < len; j++) {
			if (s[i] == s_rev[j]) {
				if (i == 0 || j == 0) {
					arr[i][j] = 1;
				}
				else {
					arr[i][j] = arr[i - 1][j - 1] + 1;
				}
				if (arr[i][j] > maxLen) {
					int beforeRev = len - 1 - j;
					if (beforeRev + arr[i][j] - 1 == i) {
						maxLen = arr[i][j];
						maxEnd = i;
					}
				}
			}
		}
	}
	int a = maxEnd - maxLen+1;
	int b = maxEnd+1;
	string res(s.begin() + a, s.begin() + b);
	return res;
}

int main() {
	string str;
    cin >> str;
	string ans = longestPalindrome(str);
    cout << ans << endl;
	return 0;
}