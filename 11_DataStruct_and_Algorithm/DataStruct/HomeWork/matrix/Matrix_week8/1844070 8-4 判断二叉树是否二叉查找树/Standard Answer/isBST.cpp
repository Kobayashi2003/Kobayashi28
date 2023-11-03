#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;
void print(vector<int>);
//assuming preorder and inorder are valide preorder and inorder traveral of a BT. It returns true if it is a BST.
bool isBST(vector<int> preorder, vector<int> inorder){
    if (preorder.size()<=1)
      return true;
    int root = preorder[0];
    vector<int>::iterator it;
    it = find(inorder.begin(),inorder.end(),root);

    if (((it==inorder.begin() ||  *max_element(inorder.begin(),it)< root)) && ( (it+1==inorder.end())||(*min_element(it+1,inorder.end()) > root))){
      vector<int> lin(inorder.begin(), it++);
      vector<int> rin(it, inorder.end());
      size_t l = lin.size();
      size_t r = rin.size();
      vector<int> lpre(preorder.begin()+1,preorder.begin()+l+1);
      vector<int> rpre(preorder.begin()+l+1,preorder.end());
//print(lpre);print(lin);print(rpre);print(rin);
      return  (isBST(lpre,lin) && isBST(rpre,rin));
   }else
    return false;
}


void print(vector<int> v){
   for (size_t i=0;i<v.size();i++){
     cout<<v[i]<<",";
   }
  cout<<endl;
}

int main(){
  int n, m, a;
  cin >> n;
for (int i=0;i<n;i++){
  vector<int> preorder, inorder;
  cin >>m;
  for (size_t i=0;i<m;i++){
    cin>>a;
    preorder.push_back(a);
  }
  for (size_t i=0;i<m;i++){
    cin>>a;
    inorder.push_back(a);
  }

 if (isBST(preorder, inorder))
     cout<<"Yes"<<endl;
 else
     cout<<"No"<<endl;
 }
 return 0;
}
