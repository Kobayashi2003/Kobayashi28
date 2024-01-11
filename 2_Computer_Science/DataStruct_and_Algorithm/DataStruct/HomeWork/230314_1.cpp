#include <iostream>
#include <string>
#include <map>
using namespace std;

class Mystack {
private:
	struct Node
	{
		char data;
		Node *next;
	};

public:
	Node *head; //栈顶指针
	int size; //栈大小

	Mystack()
	{
		head = nullptr;
		size = 0;
	}; //初始化空间

	~Mystack()
	{
		Node* q = new Node;
		while (head != nullptr)
		{
			q = head;
			head = head->next;
			delete q;
		}
	} //回收栈空间

	void push(char elem) {
		//请完成入栈函数代码
        if (head == nullptr) {
            head = new Node;
            head->data = elem;
            head->next = nullptr;
        } else {
            Node* q = new Node;
            q->data = elem;
            q->next = head;
            head = q;
        }
	};

	void pop() {
		//请完成出栈函数代码
        if (head != nullptr) {
            Node* q = head;
            head = head->next;
            delete q;
        }
	};
};

bool Symbol_matching(string str){
	Mystack stack;
	map<char, char> dic = { {'}','{'}, {']','['}, {')','('} };
    for (int i = 0; i < str.length(); ++i) {
        if (str[i] == '{' || str[i] == '[' || str[i] == '(') {
            stack.push(str[i]);
        } else if (str[i] == '}' || str[i] == ']' || str[i] == ')') {
            if (stack.head == nullptr) {
                return false;
            } else if (stack.head->data == dic[str[i]]) {
                stack.pop();
            } else {
                return false;
            }
        } else {
            continue;
        }
    }
    if (stack.head == nullptr) {
        return true;
    } else {
        return false;
    }
};

int main() {
	string str;
	bool R;
	getline(cin, str);
	R = Symbol_matching(str);
	cout << R << endl;
	return 0;
}