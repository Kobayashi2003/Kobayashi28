#include<iostream>
using namespace std;

int main(){
    int t;
    cin>>t;
    int i,j,n,front,rear;
    int a[100];
    for (i=0;i<t;i++)
    {
        cin>>n;
        for (j=0;j<n;j++)
            a[j] = j+1;
        front = 0;
        rear = j;
        while(front < rear)
        {
            cout<<a[front]<<' ';
            front++;
            a[rear] = a[front];
            front++;
            rear++;

        }
        cout<<endl;
    }
    return 0;
}