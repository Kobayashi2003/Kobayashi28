#include<string> 
#include<iostream>
using namespace std; 
typedef unsigned long long ull; 


ull Hash_a(string a, ull B){ 
	ull ans = 0; 
	for (auto ch : a)
		ans = ans * B + ch; 
	return ans;
}


bool contain(string a, string b, ull B) {
	if (a.length() < b.length()) 
		swap(a, b);
	ull hash_b = Hash_a(b, B); 
	ull hash_a = Hash_a(a.substr(0, b.length()), B); 
	if (hash_a == hash_b)  
		return true; 

	ull base = 1; 
	for (ull i = 0; i < b.length(); i++)
		base *= B;
	for (ull i = b.length(); i < a.length(); i++) { 
		hash_a = hash_a * B + a[i] - a[i - b.length()] * base; 
		if (hash_a == hash_b) 
			return true; 
	} 
	return false;
}

int main() {
	string s1, s2;  
	ull base;  
	cin >> base;  
	cin >> s1 >> s2;// bc abc   
	cout << Hash_a(s1,base) << endl;  
	if(contain(s1,s2,base)) {   
		cout<<"include"<<endl;   
	}    
	else{   
		cout<<"not include"<<endl;   
	}   
	return 0; 
} 