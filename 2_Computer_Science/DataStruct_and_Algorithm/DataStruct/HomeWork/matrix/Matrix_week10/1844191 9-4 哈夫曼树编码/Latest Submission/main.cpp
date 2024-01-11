#include <iostream>
#include <vector>
#include <string>
#include <queue>
using namespace std;

class Node {
public:
	int freq = 0;
	char key = '#';
	Node* left = nullptr;
	Node* right = nullptr;
	Node() {}
	Node(int freq_, char key_) :freq(freq_), key(key_) { }
};
class cmp {
public:
	bool operator() (Node*a, Node*b) {
		return a->freq > b->freq;
	}
};
Node* build(Node* data[], int len) {
	priority_queue<Node*, vector<Node*>, cmp> q;
	for (int i = 0; i < len; i++) {
		q.push(data[i]);
	}
	while (q.size()>=2) {
		Node* t1 = q.top();
		q.pop();
		Node* t2 = q.top();
		q.pop();
		// 合并后的节点freq为子节点freq之和，key为‘#’
		Node* t = new Node(t1->freq + t2->freq, '#');
		// 两个节点合并的顺序，频率小的放右边，频率大的放左边，频率一样字符小的右边，字符大的左边。
		// 频率和字符都相同，则先进入队列的放左边
		if (t1->freq < t2->freq) {
			t->right = t1;
			t->left = t2;
		}
		else if (t1->freq == t2->freq) {
			if (t1->key < t2->key) {
				t->right = t1;
				t->left = t2;
			}
			else {
				t->left = t1;
				t->right = t2;
			}
		}
		else {
			t->left = t1;
			t->right = t2;
		}
		q.push(t);
	}
	Node* root = q.top();
	return root;
}

void printcode(Node* root) {
	Node* t = root;
	if (t->left != nullptr) {
		printcode(t->left);
	}
	if (t->right != nullptr) {
		printcode(t->right);
	}
	if (t->left == nullptr&&t->right == nullptr) {
		cout << t->key << endl;
	}
}
int main() {
	int k;
	cin >> k;
	char val;
	int freq;
	Node* root;
	Node* data[100];
	for (int i = 0; i < k; i++) {
		cin >> val >> freq;
		data[i] = new Node(freq, val);
	}
	root = build(data,k);
	printcode(root);
	return 0;
}