#include<iostream>
#include<vector>
using namespace std;
int main(){
    int x;
    vector<int> nums;
    while(cin>>x){
        nums.push_back(x);
    }
    vector<int>::size_type nSize = nums.size();
		if (nSize <= 1)
			return nSize;

		vector<int>::size_type p = 0;
		for (vector<int>::size_type i = 1; i < nSize; ++i) {
			if (nums[i] != nums[p])
				nums[++p] = nums[i];
		}
    cout<<p+1;
}
