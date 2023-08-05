#include <iostream>
#include <vector>
#include <string>

using namespace std;
class BinaryHeap {
public:
	explicit BinaryHeap(); 
	explicit BinaryHeap(const vector<int>& items) :
		array(items.size() + 10), heapsize(items.size()) {
		for (int i = 0; i < items.size(); i++)
			array[i + 1] = items[i];
		buildHeap();
	};
	bool isEmpty() const {
		if (heapsize == 0)
			return true;
		else
			return false;
	};
	void insert(const int& x) {
		if (heapsize == array.size() - 1)
            array.resize(array.size() * 2);
        int hole = ++heapsize;
        for (; hole > 1 && x < array[hole / 2]; hole /= 2)
            array[hole] = array[hole / 2];
        array[hole] = x;
	};
	void deleteMin() {
		if (isEmpty())
			cout << "fail" << endl;
		else
			array[1] = array[heapsize--];
		percolateDown(1);
	}; //直接删除
	void deleteMin(int& minItem) {
		if (isEmpty())
			cout << "fail" << endl;
		else
			minItem = array[1];
		array[1] = array[heapsize--];
		percolateDown(1);
	};//删除并返回最小值
	int findmin() {
		return array[1];
	};
private:
	vector<int> array; // The heap array
	int heapsize; // Number of elements in heap
	void buildHeap() {
		for (int i = heapsize / 2; i > 0; i--)
			percolateDown(i);
	};
	void percolateDown(int hole) {
		int child;
		int tmp = array[hole];
		for (; hole * 2 <= heapsize; hole = child)
		{
			child = hole * 2;
			if (child != heapsize && array[child + 1] <
				array[child])
				child++;
			if (array[child] < tmp)
				array[hole] = array[child];
			else
				break;
		}
		array[hole] = tmp;
	};//向下过滤
};

int findKthLargest() {
    string s; cin >> s;
	int k; cin >> k;
    vector<int> nums;
    while (s.find(',') != string::npos) {
		int i = s.find(',');
		nums.push_back(stoi(s.substr(0, i)));
		s = s.substr(i + 1);
	}
	nums.push_back(stoi(s));
    int n = nums.size();
    BinaryHeap minheap(nums);
    for (int i = 0; i < n - k; i++) {
        minheap.deleteMin();
    }
	return minheap.findmin();
}

int main() {
	cout << findKthLargest() << endl;
	system("pause");
	return 0;
}