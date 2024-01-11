#include<iostream>
#include<vector>
using namespace std;

bool canPlaceFlowers(vector<int> f, int n) {
	int num = 0;
	int left = -1;
	f.push_back(0);
	f.push_back(1);
	f.insert(f.begin(), 0);
	f.insert(f.begin(), 1);
	for (int i = 0; i < f.size(); ++i) {
		if (f[i] == 1) {
			if (left == -1) left = i;
			else {
				num += (i - left - 2) / 2;
				left = i;
			}
		}
	}
	if (num < n) return false;
	return true;
}

int main() {
	int t;
	cin >> t;
	vector<int> f;
	int n;
	while (t--) {
		int a;
		cin >> a;
		f.push_back(a);
	}
	cin >> n;
	cout << canPlaceFlowers(f, n);
}
