#include <map>
#include <stack>
#include <string>
#include <iostream>

class expressionTree {
private:
    struct expressionTreeNode {
        enum class nodeType {B, NUM, OP}; 
        // B: blank
        // NUM: number
        // OP: operator
        nodeType type;
        char op = '\0';
        int num = .0;
        expressionTreeNode *left = nullptr, *right = nullptr;
        expressionTreeNode() : type(nodeType::B) {}       
        expressionTreeNode(int n) : type(nodeType::NUM), num(n) {}
        expressionTreeNode(char o) : type(nodeType::OP), op(o) {}
    };

    typedef expressionTreeNode node;
    node *root;

    static short P(char op) {
        std::map<char, short> priority = {
            {'+', 1}, {'-', 1}, {'*', 2}, {'/', 2}
        };
        return priority[op];
    }

    const std::map<char, char> op2opposite = {
        {'(', ')'}, {'[', ']'}, {'{', '}'}
    };

private:
    bool empty() const { return root == nullptr; }
    void delTree(node *p) {
        if (p == nullptr) return;
        if (p->left) delTree(p->left);
        if (p->right) delTree(p->right);
        delete p;
    }

    node* inOrd2Tree(const std::string expr) {
        node *sub_root = nullptr; 
        node *current_node = nullptr;

        for (size_t i = 0; i < expr.size(); ++i) {
            char ch = expr[i];
            if (ch == ' ') continue;
            
            if (op2opposite.find(ch) != op2opposite.end()) {
                std::string sub_expr = "";
                std::stack<char> pair_stack;
                pair_stack.push(ch);
                while (1) {
                    if (i == expr.size() - 1) 
                        throw "Error: unmatched parentheses."; 

                    ch = expr[++i];
                    if (ch == ' ') continue;
                    if (op2opposite.find(ch) != op2opposite.end()) {
                        pair_stack.push(ch);
                    }
                    else if (ch == op2opposite.at(pair_stack.top())) {
                        pair_stack.pop();
                        if (pair_stack.empty()) break;
                    }
                    sub_expr += ch;
                }
                node *sub_tree = inOrd2Tree(sub_expr);
                if (sub_root == nullptr) 
                    current_node = sub_tree;
                else
                    current_node->right = sub_tree;  
            }

            else if (ch > '0' && ch < '9') {
                int num = ch - '0';
                while (i < expr.size() - 1 && expr[i + 1] > '0' && expr[i + 1] < '9') {
                    num = num * 10 + expr[++i] - '0';
                }
                node *num_node = new node(num);
                if (sub_root == nullptr)
                    current_node = num_node;
                else
                    current_node->right = num_node;
            }

            else if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
                node *op_node = new node(ch);
                if (sub_root == nullptr) {
                    sub_root = op_node;
                    sub_root->left = current_node;
                    current_node = sub_root;
                    continue;
                }
                switch (P(ch) - P(sub_root->op)) {
                case 0:
                    op_node->left = sub_root;
                    sub_root = current_node = op_node;
                    break;
                case 1:
                    op_node->left = sub_root->right;
                    sub_root->right = op_node;
                    current_node = op_node;
                    break;
                case -1:
                    op_node->left = sub_root;
                    sub_root = current_node = op_node;
                    break;
                default:
                    throw "Error: invalid expression.";
                }
            }
        }
        if (sub_root == nullptr) return current_node;
        return sub_root;
    }

    node* postOrd2Tree(const std::string expr) {
        std::stack<node*> node_stack;
        for (size_t i = 0; i < expr.size(); ++i) {
            char ch = expr[i];
            if (ch == ' ') continue;
            else if (ch > '0' && ch < '9') {
                int num = ch - '0';
                while (i < expr.size() - 1 && expr[i + 1] > '0' && expr[i + 1] < '9') {
                    num = num * 10 + expr[++i] - '0';
                }
                node *num_node = new node(num);
                node_stack.push(num_node);  
            }
            else if (ch == '+' || ch == '-' || ch == '*' || ch == '/') {
                node *op_node = new node(ch);
                op_node->right = node_stack.top();
                node_stack.pop();
                op_node->left = node_stack.top();
                node_stack.pop();
                node_stack.push(op_node);
            }
        }
        return node_stack.top();
    }

    void postOrder(node *p) {
        if (p->left) postOrder(p->left);
        if (p->right) postOrder(p->right);
        if (p->type == node::nodeType::NUM) std::cout << p->num << ' ';
        else if (p->type == node::nodeType::OP) std::cout << p->op << ' ';
    }

    void preOrder(node *p) {
        if (p->type == node::nodeType::NUM) std::cout << p->num << ' ';
        else if (p->type == node::nodeType::OP) std::cout << p->op << ' ';
        if (p->left) preOrder(p->left);
        if (p->right) preOrder(p->right);
    }

    void cal(node *p) {
        if (p->left) cal(p->left);
        if (p->right) cal(p->right);
        if (p->type == node::nodeType::OP) {
            switch (p->op) {
                case '+': p->num = p->left->num + p->right->num; break;
                case '-': p->num = p->left->num - p->right->num; break;
                case '*': p->num = p->left->num * p->right->num; break;
                case '/': p->num = p->left->num / p->right->num; break;
            }
        }
    }


public:
    expressionTree() : root(nullptr) {}
    ~expressionTree() { delTree(root); }

    void inOrder2Tree(const std::string expr) { clear(); root = inOrd2Tree(expr); }
    void postOrder2Tree(const std::string expr) { clear(); root = postOrd2Tree(expr); }

    void postOrder() { postOrder(root); std::cout << std::endl; }
    void preOrder() { preOrder(root); std::cout << std::endl; }

    void cal() { cal(root); std::cout << root->num << std::endl; }

    void clear() { delTree(root); root = nullptr; }

};


int main() {

    expressionTree expTree;

    std::cout << "in order to expression tree" << std::endl;
    expTree.inOrder2Tree("1 + 6 * [ (1 * 8) + 2 ] * ( 6 / 2 ) + 5 * 6");
    expTree.postOrder();
    expTree.preOrder();
    expTree.cal();

    std::cout << "post order to expression tree" << std::endl;
    expTree.postOrder2Tree("1 6 1 8 * 2 + * 6 2 / * + 5 6 * +");
    expTree.postOrder();
    expTree.preOrder();
    expTree.cal();

    return 0;
}