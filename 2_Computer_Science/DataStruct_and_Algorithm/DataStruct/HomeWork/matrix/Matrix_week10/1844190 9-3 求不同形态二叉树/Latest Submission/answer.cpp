
#include <iostream>
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <string>
#include <map>
#include <queue>
#include <vector>
#include <stack>
#include <climits>
using namespace std;
      
int main()
{
    string s1,s2;
    while(cin>>s1>>s2)
    {
        int count=1;
        for(int i=1;i<s1.size();++i)
        {
            int index=s2.find(s1[i]);
            if(s2[index+1]==s1[i-1]) count*=2;
        }
        cout<<count;
    }

    return 0;
}