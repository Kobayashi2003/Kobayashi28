#include <iostream>
using namespace std;

template<typename T>
class HashMap {
public:
	struct HashValue {
		T value;
		bool useful;
		HashValue() :value(0), useful(true) {}
	};
	int k;
	HashValue* head;
	HashMap<T>(int capacity) : k(capacity) {
		head = new HashValue[capacity];
	}

	void insert(T v) {
        int index = v % k;
        while (1) {
            if (head[index].useful) {
                head[index].value = v;
                head[index].useful = false;
                break;
            }
            index = (index + 1) % k;
        }
	}

	bool remove(T v) {
        int index = v % k;
        for (int i = 0; i < k; ++i) {
            if (!head[index].useful && head[index].value == v) {
                head[index].useful = true;
                return true;
            }
            index = (index + 1) % k;
        }
        return false;
	}

	bool search(T v) {
        int index = v % k;
        for (int i = 0; i < k; ++i) {
            if (!head[index].useful && head[index].value == v)
                return true;
            index = (index + 1) % k;
        }
        return false;
	}
};

int main() {
	int c, n; 
	cin >> c >> n; 
	HashMap<int> map(c); 
	while (n--) { 
		cin >> c; 
		map.insert(c); 
	}
	cin >> n; 
	while (n--) { 
		cin >> c; 
		if (!map.remove(c)) 
			cout << "Delete Error" << endl; 
	} 
	cin >> n; 
	while (n--) {
		cin >> c;
		if (map.search(c))
			cout << "True" << endl; 
		else 
			cout << "False" << endl;
	}
	return 0;
}