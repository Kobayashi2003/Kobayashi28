#include<iostream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;


int lengthofLongestSubString(string s) {
	int n = s.length();
	set<char> set;
	int ans = 0;
	int i = 0, j = 0;
	while (i < n&&j < n) {
		if (set.find(s[j]) == set.end()) {
			set.insert(s[j]);
			j++;
			ans = max(ans, j - i);
		}
		else {
			set.erase(s[i]);
			i++;
		}
	}
	return ans;
}
int main() {
	string s;
    cin >> s;
	int ans = lengthofLongestSubString(s);
	cout << ans << endl;
	return 0;
}