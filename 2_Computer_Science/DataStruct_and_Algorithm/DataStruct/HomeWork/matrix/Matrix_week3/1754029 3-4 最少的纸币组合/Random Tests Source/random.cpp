#include<iostream>
#include<stdlib.h>
#include<time.h>
using namespace std; 
#define random(x) (rand()%x)
 
int main() {
	srand((int)time(0));	  
	int n=random(100)%100+1;
	int k=random(100);
	cout<<n<<" "<<k<<endl;
    for (int i = 0; i < k; i++) {
        cout << random(200) <<" ";
    }
    return 0;
}
