#include <iostream>

class Node {
public:
    Node(int elem_, Node* lchild_ = NULL, Node* rchild_ = NULL, Node* parent_ = NULL, int balance_ = 0) {
        _elem = elem_;
        _lchild = lchild_;
        _rchild = rchild_;
        _parent = parent_;
        _balance = balance_;
    }
    bool hasLeftChild() {//判断是否有左孩子结点
        return _lchild != NULL;
    }
    bool hasRightChild() {//判断是否有右孩子结点
        return _rchild != NULL;
    }
    bool hasParent() {//判断是否有父母结点
        return _parent != NULL;
    }
    bool isLeftChild() {//判断是否为父母结点的左孩子结点
        return _parent->_lchild == this;
    }
    bool isRightChild() {//判断是否为父母结点的右孩子结点
        return _parent->_rchild == this;
    }
public:
    int _elem = 0;
    int _balance = 0;
    Node* _lchild = NULL;
    Node* _rchild = NULL;
    Node* _parent = NULL;

};

class AVLtree {
public:
    AVLtree(Node* root_ = NULL) {
        _root = root_;
    }
    void rotateL(Node* & root_) {//当前结点作根节点对应的子树左旋
        Node *tmp = root_->_rchild;
        root_->_rchild = tmp->_lchild;
        if (tmp->_lchild != nullptr) {
            tmp->_lchild->_parent = root_;
        }
        tmp->_lchild = root_;
        tmp->_parent = root_->_parent;
        root_->_parent = tmp;
        updateBalance(root_);
        updateBalance(tmp);
       
        root_ = tmp;

        return;
    }
    void rotateR(Node* & root_) {//当前结点作根节点对应的子树右旋
        Node *tmp = root_->_lchild;
        root_->_lchild = tmp->_rchild;
        if (tmp->_rchild != nullptr) {
            tmp->_rchild->_parent = root_;
        }
        tmp->_rchild = root_;
        tmp->_parent = root_->_parent;
        root_->_parent = tmp;
        updateBalance(root_);
        updateBalance(tmp);

        root_ = tmp;

        return;
    }

    void rebalance(Node* & node_) {//平衡AVL树
        if (node_->_balance > 1) {
            if (node_->_lchild->_balance > 0) {
                rotateR(node_);
            }
            else {
                rotateL(node_->_lchild);
                rotateR(node_);
            }
        }    
        else if (node_->_balance < -1) {
            if (node_->_rchild->_balance < 0) {
                rotateL(node_);
            }
            else {
                rotateR(node_->_rchild);
                rotateL(node_);
            }
        }

        return;
    }

    int getHeight(Node *node_) {
        if (node_ == nullptr) return 0;
        int lheight = getHeight(node_->_lchild);
        int rheight = getHeight(node_->_rchild);
        return lheight > rheight ? lheight + 1 : rheight + 1;
    }

    void updateBalance(Node* node_) {//更新结点平衡值，保证在-1~1

        node_->_balance = getHeight(node_->_lchild) - getHeight(node_->_rchild);

        return;
    }

    void insert(int elem_, Node* & node_) {//插入结点
        if (_root == nullptr) {
            _root = new Node(elem_);
            return;
        }
        if (elem_ < node_->_elem) {
            if (node_->_lchild == nullptr) {
                node_->_lchild = new Node(elem_, nullptr, nullptr, node_);
            }
            else {
                insert(elem_, node_->_lchild);
            }
        }
        else if (elem_ > node_->_elem) {
            if (node_->_rchild == nullptr) {
                node_->_rchild = new Node(elem_, nullptr, nullptr, node_);
            }
            else {
                insert(elem_, node_->_rchild);
            }
        }
        updateBalance(node_);
        rebalance(node_);
        return;
    }

    void pre_order(Node* node_) {//先序遍历
        if (node_ != NULL) {
            std::cout << node_->_elem << std::endl;
            pre_order(node_->_lchild);
            pre_order(node_->_rchild);
        }
        return;
    }
public:
    Node* _root = NULL;

};

int main() {
    int data_in;
    AVLtree avltree;
    while (std::cin >> data_in) {
        avltree.insert(data_in, avltree._root);
        if (std::cin.get() == '\n') break;
    }
    avltree.pre_order(avltree._root);
    return 0;
}
