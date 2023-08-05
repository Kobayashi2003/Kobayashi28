#include <iostream>
#include <vector>
using namespace std;

class BSTNode {
public:
    int key; // 关键字
    BSTNode *left; // 左子节点
    BSTNode *right; // 右子节点
    BSTNode *parent; // 父节点
    BSTNode(int k = 0, BSTNode *l = NULL, BSTNode *r = NULL, BSTNode *p = NULL) : key(k), left(l), right(r), parent(p) {}; // 初始化列表
};

class BSTree {
public:
    BSTree() :root(NULL) {}; // 构造函数

    ~BSTree() // 析构函数
    {
        destroy();
    };

    void insert(int key) // 将 key 节点插入到二叉树中
    {
        BSTNode *z = new BSTNode(key, NULL, NULL, NULL); // 根据插入的 key 生成新的二叉树节点 (z)
        if (z == NULL) {
            return; // 如果 z 里面的值为空，则停止函数的执行
        }
        insert(root, z); // 把新生的节点 (z) 传入树根
    }

    void PreOrder()
    {
        PreOrder(root); // 传入根节点
    }

    void PostOrder()
    {
        PostOrder(root); // 传入根节点
    }

    BSTNode *search(int key)
    {
        return search(root, key); // 传入根节点和待查找的关键字 key
    }

    BSTNode *successor(BSTNode *x) // 找节点 (x) 的后继节点，也就是该节点的右子树中的最小节点
    {
        BSTNode *y = NULL;
        if (x->right != NULL) {
            return minimum(x->right);
        }
        // 如果 x 没有右子节点。则 x 有以下两种可能：
        // （1） x 是"一个左子节点"，则"x 的后继节点"为 "它的父节点"。
        // （2） x 是"一个右子节点"，则查找"x 的最低的父节点，并且该父节点要具有左子节点"，找到的这个"最低的父节点"就是"x 的后继节点"。
        y = x->parent;
        while (y != NULL && x == y->right) {
            x = y;
            y = y->parent;
        }
        return y;
    }

    BSTNode *predecessor(BSTNode *x) // 找节点 (x) 的前驱节点是该节点的左子树中的最大节点。
    {
        BSTNode *y = NULL;
        if (x->left != NULL) {
            return maximum(x->left);
        }
    }

    void remove(int key) // 删除二叉树 (tree) 中的节点 (z)，并返回被删除的节点
    {
        BSTNode *z, *node;
        z = search(root, key); // 根据给定的 key，查找树中是否存在 key 节点
        if (z != NULL) {
            node = remove(root, z); // 传入树根以及待删除的节点 (z)
            if (node != NULL) {
                delete node;
                this->PostOrder();
            }
        }
        else {
            cout << "Delete Error";
        }
    }

    void destroy() // 销毁二叉树
    {
        destroy(root);
    }

private:
    BSTNode *root; // 根节点

    void PreOrder(BSTNode *tree) 
    {
        // 前序二叉树遍历
        if (tree != nullptr) {
            cout << tree->key << " ";
            PreOrder(tree->left);
            PreOrder(tree->right);
        }
    }

    void PostOrder(BSTNode *tree) 
    {
        // 后序二叉树遍历
        if (tree != nullptr) {
            PostOrder(tree->left);
            PostOrder(tree->right);
            cout << tree->key << " ";
        }
    }

    BSTNode *minimum(BSTNode *tree) // 查找最小节点：返回 tree 为根节点的二叉树的最小节点。
    {
        if (tree == NULL) {
            return NULL;
        }
        while (tree->left != NULL) {
            tree = tree->left;
        }
        return tree;
    }

    BSTNode *maximum(BSTNode *tree) // 查找最大节点：返回 tree 为根节点的二叉树的最大节点。
    {
        while (tree->right != NULL) {
            tree = tree->right;
        }
        return tree;
    }

    BSTNode *search(BSTNode *x, int key) 
    {
        // 递归实现，在二叉搜索树 x“中查找 key 节点
        if (x == nullptr || x->key == key) 
            return x;
        else if (key < x->key) 
            return search(x->left, key);
        else 
            return search(x->right, key);
    }

    void insert(BSTNode *&tree, BSTNode *z) 
    {
        // 将节点 (z) 插入到二叉搜索树 (tree) 中
        if (tree == nullptr)
            tree = z;
        else if (z->key < tree->key) 
            insert(tree->left, z);
        else 
            insert(tree->right, z);
    }

    BSTNode *remove(BSTNode *tree, BSTNode *z) 
    {
        // 删除二叉搜索树 (tree) 中的节点 (z)，并返回被删除的节点
        if (z->left != nullptr && z->right != nullptr) {
            BSTNode *rmin = minimum(z->right);
            z->key = rmin->key;
            return remove(tree, rmin);
        } else {
            BSTNode *parent = nullptr;
            while (tree != nullptr && tree != z) {
                parent = tree;
                if (z->key < tree->key) {
                    tree = tree->left;
                } else {
                    tree = tree->right;
                }
            }
            BSTNode *child = (z->left != nullptr) ? z->left : z->right;
            if (parent == nullptr) {
                tree = child;
            } else {
                if (parent->left == z) {
                    parent->left = child;
                } else {
                    parent->right = child;
                }
            }
            return z;
        }
    }

    void destroy(BSTNode *&tree) // 销毁二叉树
    {
        if (tree == NULL) {
            return; // 停止函数的执行
        }
        if (tree->left != NULL) {
            return destroy(tree->left);
        }
        if (tree->right != NULL) {
            return destroy(tree->right);
        }
        delete tree;
        tree = NULL;
    }
};

vector<int> strToArr(string str){
    int len = str.size();
    vector<int> res;
    bool key = false;
    for (int i = 0; i < len; i++){
        if (str[i] >= '0' && str[i] <= '9') {// 遇到数字
            if (key) // 不是数字的第一个字符
                *(res.end() - 1) = *(res.end() - 1) * 10 + str[i] - '0';
            else {
                int tmp = str[i] - '0';
                if (i>=0 && str[i - 1] == '-') // 负数
                    tmp *= -1;
                res.push_back(tmp); // 将数字的第一个字符添加到数组中
                key = true;
            }
        }
        else // 遇到的不是数字
            key = false;
    }
    return res;
}

int main(void)
{
    BSTree *tree = new BSTree();
    string s;
    getline(cin, s);
    vector<int> vec;
    vec = strToArr(s);
    for (int i = 0; i < vec.size(); i++) {
        tree->insert(vec[i]); // 调用插入函数，生成二叉查找树
    }
    int n, m;
    cin >> n;
    int insertnum, delectnum;
    for (int i = 0; i < n; i++) {
        cin >> insertnum;
        tree->insert(insertnum);
        tree->PreOrder();
        cout << endl;
    }
    cin >> m;
    for (int i = 0; i < m; i++) {
        cin >> delectnum;
        tree->remove(delectnum);
        cout << endl;
    }
    tree->destroy();
    return 0;
}