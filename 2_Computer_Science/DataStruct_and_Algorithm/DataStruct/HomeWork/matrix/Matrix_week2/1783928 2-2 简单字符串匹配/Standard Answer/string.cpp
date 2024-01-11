#include <iostream>
#include <string>
using namespace std;
int main(){
    int test_case;
    cin>>test_case;
    while(test_case--){
        string str1,str2;
        cin>>str1>>str2;
        int length=str1.length();
        bool judge=true;
        for(int i=0;i<length;i++){
            if(str1.find(str2)==string::npos){
                str1=str1+str1[i];
                str1[i]=0;
            }
            else{
                judge=false;
                cout<<"True"<<endl;
                break;
            }
        }
        if(judge) cout<<"False"<<endl;
    }
    return 0;
}
