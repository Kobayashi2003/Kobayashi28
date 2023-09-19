#include<iostream>
#include<vector>
#include<limits.h>
using namespace std;

int main(){
	int s,n;
	cin>>s>>n;
	vector<int> nums(n);
	for(int i=0;i<n;i++) cin>>nums[i];
	
	int ans = INT_MAX;
    int left = 0;
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += nums[i];
        while (sum >= s) {
            ans = min(ans, i + 1 - left);
            sum -= nums[left++];
        }
    }
    ans = (ans != INT_MAX) ? ans : 0;
	cout<<ans;
	return 0;
}
