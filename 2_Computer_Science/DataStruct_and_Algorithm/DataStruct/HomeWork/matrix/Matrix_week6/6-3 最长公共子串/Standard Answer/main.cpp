
#include<iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int longestCommonSubString(string s1, string s2) {
	if (s1.empty() || s2.empty()) {
		return 0;
	}

	int len1 = s1.length();
	int len2 = s2.length();
	vector<vector<int> > arr;
	vector<int> temp;
	for (int i = 0; i < len2; i++) {
		temp.push_back(0);
	}
	for (int i = 0; i < len1; i++) {
		arr.push_back(temp);
	}
	int maxLen = 0;
	for (int i = 0; i < len1; i++) {
		for (int j = 0; j < len2; j++) {
			if (s1[i] == s2[j]) {
				if (i == 0 || j == 0) {
					arr[i][j] = 1;
				}
				else {
					arr[i][j] = arr[i - 1][j - 1] + 1;
					maxLen = max(arr[i][j], maxLen);
				}

			}
		}
	}
	return maxLen;
}

int main() {

	string s2;
	string s1;
	cin >> s1;
	cin >> s2;
	int ans = longestCommonSubString(s1,s2);
	cout << ans << endl;
	return 0;
}
