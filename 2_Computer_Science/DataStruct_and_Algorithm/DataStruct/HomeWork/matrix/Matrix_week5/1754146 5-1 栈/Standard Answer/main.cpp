#include <iostream>
#include<stack>
#include<string>
using namespace std;
int main(int argc, const char * argv[]) {
    string str;
    int yes = 0;
    while(getline(cin,str))
    {
//        cout<<str<<endl;
        if(str.size()==0)//则为空行
        {
            if(yes == 1)
            { //cout<<"退出了"<<endl;
                break;
            }
            else
            {
                yes = 1;
                continue;
            }
        }
        yes = 0;
        stack <int> mystack1;
        stack <int> mystack2;
        int N = atoi(str.c_str());
//        cin>>N;
        for(int i =0;i<N;i++)
        {
            getline(cin,str);
//            cout<<str<<endl;
            int k;
            k = atoi(str.substr(0,1).c_str());
//            cout<<k<<endl;
            int num;
            if(k==0)
            {
                num = atoi(str.substr(2).c_str());
                if(!mystack1.empty())
                {
                    mystack1.push(num);
                    int tmp = mystack2.top();
                    if(tmp<num)
                    {
                        num = tmp;
                    }
                    mystack2.push(num);
                }
                else
                {
                    mystack2.push(num);
                    mystack1.push(num);
                }
            }

            if(k==1)
            {
                if(!mystack1.empty())
                {
                    mystack1.pop();
                    mystack2.pop();
                }
            }
            if(k==2)
            {
                if(!mystack1.empty())
                {
                    int tmp = mystack1.top();
                    cout<<tmp<<endl;
                }
                else
                    cout<<-1<<endl;
            }
            if(k==3)
            {
                if(!mystack2.empty()){
                    int tmp = mystack2.top();
                    cout<<tmp<<endl;
                }
                else
                    cout<<-1<<endl;
            }
        }

    }


    return 0;
}
