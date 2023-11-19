#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;


typedef int T;

struct treeNode {
  T data;
  struct treeNode *left, *right;
 
  treeNode(T d, treeNode *l=NULL, treeNode *r=NULL):data(d),left(l),right(r){};
};

void release(treeNode * t){
  if (t) {
   release(t->left); 
   release(t->right);
   delete t;
  }
    
} 
/*
bool insert(treeNode *&root, const T d)
// Pre: t is a binary search tree
//Post: d is inserted in t if it is not on the tree
//and the resulting tree is a binary search tree
{
  return insertR(root, d);
}
*/

void  insert(treeNode *& t, const T d)
// Pre: t is a binary search tree
//Post: d is inserted in t if it is not on the tree
//and the resulting tree is a binary search tree
{

 if (!t) {
   t = new treeNode(d);
  }
 else  if (d<t->data) 
       insert(t->left,d);     
 else if (d>t->data) 
        insert(t->right, d);
  

}




typedef pair<treeNode *, int> beta;

int width(const treeNode *root, int &l, vector<int> &w){

 if (root==NULL){
   //w.push_back(-1);
   l=-1;
   return 0;
 }
 w.clear();
 w.push_back(1);
 int ll=0; //level of left subtree
 int lr=0; //level of right subtree
 vector<int>lw, rw;//width vector of the left and right subtrees 
 width(root->left, ll, lw);
 width(root->right, lr, rw);
 int i=0;
 l = max(lr, ll) +1;
//cout <<"l : "<<l<<endl;
 while(i<=ll && i<=lr){
   w.push_back(lw[i]+rw[i]);
   i++;
  }
 while(i<=ll){
   w.push_back(lw[i]);
   i++;
  }
 while(i<=lr){
   w.push_back(rw[i]);
   i++;
 }
   
 return 0;
}     
     
     
void print(treeNode *root){
  if (root){
     cout <<root->data<<" ";
     print(root->left);
     print(root->right);
  }

}





int main(){
 
// treeNode *root=NULL;
 int n,m,x;
  cin>>n;
/*  srand(time(0));
  for (int i=0;i<n;i++){
  int k = rand()%100;
   cout << k<< "  ";
   insert(root, k);
  }
*/
  while (n--){
    cin >> m;
    treeNode *root = NULL;
    while (m--){
       cin >> x;
       insert(root,x);
    }
      int l=0;
      vector<int> w;
      width(root, l, w);  
      cout << *max_element(w.begin(),w.end())<<endl;
      release(root);
    }


  return 0;

};
