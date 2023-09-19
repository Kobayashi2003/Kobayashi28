#include<iostream>
#include<algorithm>
using namespace std;
int main(){
	int values[4][4];
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			cin>>values[i][j];
		}
	}
	int dp[4][4];
	dp[0][0]=values[0][0];
         
    for(int i=0;i<4;i++)
        for(int j=0;j<4;j++)
        {
        if(!j && !i)
            continue;
        else
            dp[i][j] = max((j==0)?0:dp[i][j-1],(i==0)?0:dp[i-1][j])+ values[i][j];
             
        }
    cout<<dp[3][3];
	return 0;
}
