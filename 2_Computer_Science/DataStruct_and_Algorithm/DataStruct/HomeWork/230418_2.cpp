// BTree.cpp : 定义控制台应用程序的入口点。
//本程序没有考虑磁盘读写，磁盘读写主要在数据库中应用
#include<iostream>
#include<fstream>
#include<vector>
using namespace std;
//定义 B 树的最小度数
const int M = 2;
//键值个数的上限
const int KEY_MAX = 2 * M - 1;
//键值个数的下限
const int KEY_MIN = M - 1;
//孩子结点个数的上限
const int CHILD_MAX = KEY_MAX + 1;
//孩子结点个数的下限
const int CHILD_MIN = KEY_MIN + 1;

//定义结点
template<class T>
class Node {
public:
	bool isLeaf; //是否为叶子节点
	vector<T> keyValue; //键值容器
	vector<Node*> pChild; //孩子指针容器
	int keyNum; //存储键值的个数
	//构造初始化
	Node() {
		isLeaf = true;
		keyNum = 0;
		keyValue.resize(KEY_MAX);
		pChild.resize(CHILD_MAX);
	}
};
template<class T>
class BTree {
private:
	//定义根结点
	Node<T>* root;
public:
	//初始化一棵空的 B 树
	BTree();
	//析构释放 B 树
	~BTree();
	//得到根节点
	Node<T>* getRootNode();
	//查找节点
	bool search(Node<T>* p, T key);
	//释放 B 树空间
	void clearBTree(Node<T>* p);
	//分裂 B 树中的结点
	void splitChild(Node<T>* p, int index);
	//插入关键字
	bool insertKey(T key);
	void insertNonFull(Node<T>* p, T key);
	//合并结点
	void mergeChild(Node<T>* p, int index);
	//找前驱
	T getPredecessor(Node<T>* p);
	//找后继
	T getSuccessor(Node<T>* p);
	//删除结点
	bool deleteKey(T key);
	void recursiveDeleteKey(Node<T>* p, T key);
	//遍历 B 树
	void printBTree(Node<T>* p, int count);
	//输出 B 树最右结点的最右关键字
	void printBTree_right(Node<T>* p);
};
template<class T>
BTree<T>::BTree() {
	root = new Node<T>();
}
template<class T>
BTree<T>::~BTree() {
	clearBTree(root);
}
template<class T>
bool BTree<T>::search(Node<T>* p, T key) {
	int i = 0;
	//查找 key 可能在的位置
	while (i < p->keyNum && key > p->keyValue[i]) {
		++i;
	}
	//找到了
	if (i < p->keyNum && key == p->keyValue[i]) {
		return true;
	}
	else {
		//叶子结点
		if (p->isLeaf) {
			return false;
		}
		else {
			//递归查找
			return search(p->pChild[i], key);
		}
	}
}

template<class T>
void BTree<T>::clearBTree(Node<T>* p) {
	if (p != NULL) {
		if (!p->isLeaf) {
			for (int i = 0; i <= p->keyNum; ++i) {
				clearBTree(p->pChild[i]);//递归释放
			}
		}
		delete p;
		p = NULL;
	}
}

template<class T>
void BTree<T>::splitChild(Node<T>* p, int index) {
	//新建分裂后的右子树
	Node<T>* pRight = new Node<T>();
	//分裂后的左子树
	Node<T>* pLeft = p->pChild[index];
	pRight->isLeaf = pLeft->isLeaf;
	pRight->keyNum = KEY_MIN;
	//将左子树中后边的值赋给右子树
	for (int i = 0; i < KEY_MIN; ++i) {
        pRight->keyValue[i] = pLeft->keyValue[i + KEY_MIN + 1];
    }
	//如果左子树不为叶节点，将其孩子对应的孩子赋给右子树
	if (!pLeft->isLeaf) {
        for (int i = 0; i < CHILD_MIN; ++i) {
            pRight->pChild[i] = pLeft->pChild[i + CHILD_MIN];
        }
    }
	//更改左子树的大小
	pLeft->keyNum = KEY_MIN;
	//上溢结点的值右移
	//孩子右移
	for (int i = p->keyNum; i > index; --i) {
        p->pChild[i + 1] = p->pChild[i];
        p->keyValue[i] = p->keyValue[i - 1];
    }
	//上溢结点插入相应的值
	p->keyValue[index] = pLeft->keyValue[KEY_MIN];
	//孩子更改为右子树
	p->pChild[index + 1] = pRight;
	++p->keyNum;
}

template<class T>
bool BTree<T>::insertKey(T key) {
    Node<T>* p = root;
    //根结点满了，分裂
    if (p->keyNum == KEY_MAX) {
        Node<T>* pNew = new Node<T>();
        root = pNew;
        pNew->isLeaf = false;
        pNew->keyNum = 0;
        pNew->pChild[0] = p;
        splitChild(pNew, 0);
        insertNonFull(pNew, key);
    }
    else {
        insertNonFull(p, key);
    }
    return true;
}

template<class T>
void BTree<T>::insertNonFull(Node<T>* p, T key) {
    int i = p->keyNum - 1;
    //如果是叶子结点
    if (p->isLeaf) {
        //找到插入的位置
        while (i >= 0 && key < p->keyValue[i]) {
            p->keyValue[i + 1] = p->keyValue[i];
            --i;
        }
        //插入
        p->keyValue[i + 1] = key;
        ++p->keyNum;
    }
    else {
        //找到插入的位置
        while (i >= 0 && key < p->keyValue[i]) {
            --i;
        }
        ++i;
        //如果子结点满了，分裂
        if (p->pChild[i]->keyNum == KEY_MAX) {
            splitChild(p, i);
            //如果插入的值大于分裂后的值，插入到右子树
            if (key > p->keyValue[i]) {
                ++i;
            }
        }
        insertNonFull(p->pChild[i], key);
    }
}

template<class T>
void BTree<T>::mergeChild(Node<T>* p, int index) {
	Node<T>* pChild1 = p->pChild[index];
	Node<T>* pChild2 = p->pChild[index + 1];
	//根本算法导论情况 2c，结点 p 的左右子结点均为 t-1 个关键字，合并两个子结点
	pChild1->keyNum = KEY_MAX;
	//父亲结点上移
	pChild1->keyValue[KEY_MIN] = p->keyValue[index];
	//合并到 child1
	for (int i = 0; i < KEY_MIN; ++i) {
        pChild1->keyValue[i + KEY_MIN + 1] = pChild2->keyValue[i];
    }
	//child1 为内部结点处理其子结点
	if (!pChild1->isLeaf) {
        for (int i = 0; i < CHILD_MIN; ++i) {
            pChild1->pChild[i + CHILD_MIN] = pChild2->pChild[i];
        }
    }
	//处理父亲结点
	for (int i = index; i < p->keyNum - 1; ++i) {
        p->keyValue[i] = p->keyValue[i + 1];
        p->pChild[i + 1] = p->pChild[i + 2];
    }
}

template<class T>
T BTree<T>::getPredecessor(Node<T>* p) {
	//p 为所属结点的左子结点
	while (!p->isLeaf) {
		p = p->pChild[p->keyNum];
	}
	return p->keyValue[p->keyNum - 1];
}

template<class T>
T BTree<T>::getSuccessor(Node<T>* p) {
	//p 为所属结点的右子结点
	while (!p->isLeaf) {
		p = p->pChild[0];
	}
	return p->keyValue[0];
}

template<class T>
bool BTree<T>::deleteKey(T key) {
	if (!search(root, key)) {
		return false;
	}
	//考虑特殊情况
	if (root->keyNum == 1 && root->isLeaf) {
        root->keyNum = 0;
        return true;
    }
}
template<class T>
void BTree<T>::recursiveDeleteKey(Node<T>* p, T key) {
	int i = 0;
	while (i<p->keyNum && key > p->keyValue[i]) {
		++i;
	}
	//关键字在 p 内，接下来考虑各种情况
	if (i < p->keyNum && key == p->keyValue[i]) {
        //情况 1，p 为叶子结点，直接删除
        if (p->isLeaf) {
            for (int j = i; j < p->keyNum - 1; ++j) {
                p->keyValue[j] = p->keyValue[j + 1];
            }
            --p->keyNum;
        }
        //情况 2，p 为内部结点，且其左子结点至少有 t 个关键字
        else if (p->pChild[i]->keyNum >= CHILD_MIN) {
            T predecessor = getPredecessor(p->pChild[i]);
            p->keyValue[i] = predecessor;
            recursiveDeleteKey(p->pChild[i], predecessor);
        }
        //情况 3，p 为内部结点，且其左子结点至少有 t 个关键字
        else if (p->pChild[i + 1]->keyNum >= CHILD_MIN) {
            T successor = getSuccessor(p->pChild[i + 1]);
            p->keyValue[i] = successor;
            recursiveDeleteKey(p->pChild[i + 1], successor);
        }
        //情况 4，p 为内部结点，且其左右子结点均有 t-1 个关键字
        else {
            mergeChild(p, i);
            recursiveDeleteKey(p->pChild[i], key);
        }
    }
}
template<class T>
void BTree<T>::printBTree(Node<T>* p, int count) {
	if (p == NULL) {
        return;
    }
    for (int i = 0; i < count; ++i) {
        cout << " ";
    }
    for (int i = 0; i < p->keyNum; ++i) {
        cout << p->keyValue[i] << " ";
    }
    cout << endl;
    for (int i = 0; i <= p->keyNum; ++i) {
        printBTree(p->pChild[i], count + 1);
    }
}

template<class T>
void BTree<T>::printBTree_right(Node<T>* p) {
	if (p == NULL) {
        return;
    }
    // just print the rightmost key of each layer
    cout << p->keyValue[p->keyNum - 1] << " ";
    printBTree_right(p->pChild[p->keyNum]);
}

template<class T>
Node<T>* BTree<T>::getRootNode() {
	return root;
}

int main() {
	BTree<int>* root = new BTree<int>();
	int data, len;
	cin >> len;
	/*cin >> data;*/
	while (len != 0) {
		cin >> data;
		root->insertKey(data);
		len--;
	}
	root->printBTree_right(root->getRootNode());
	return 0;
}