#include<iostream>
#include <vector>
using namespace std;

template <typename T>
const T & median3(vector<T> & arr, int low, int high);

template<typename T>
void quicksort(vector<T> &arr, int low, int high) {
    if (low + 10 <= high) {
        const T & pivot = median3(arr, low, high);
        int i = low, j = high - 1;
        for (;;) {
            while (arr[++i] < pivot) {}
            while (pivot < arr[--j]) {}
            if (i < j) {
                swap(arr[i], arr[j]);
            }
            else {
                break;
            }
        }
        swap(arr[i], arr[high - 1]);
        quicksort(arr, low, i - 1);
        quicksort(arr, i + 1, high);
    }
    else {
        for (int i = low; i <= high; i++) {
            for (int j = i; j > low && arr[j] < arr[j - 1]; j--) {
                swap(arr[j], arr[j - 1]);
            }
        }
    }
}

template<typename T>
const T & median3(vector<T> & arr, int low, int high) {
    int center = (low + high) / 2;
    if (arr[center] < arr[low]) {
        swap(arr[center], arr[low]);
    }
    if (arr[high] < arr[low]) {
        swap(arr[high], arr[low]);
    }
    if (arr[high] < arr[center]) {
        swap(arr[high], arr[center]);
    }

    swap(arr[center], arr[high - 1]);

    return arr[high - 1];
}


int main() {
	vector<int> vec;
	int num;
	cin >> num;
	for (int i = 0; i < num; i++) {
		int value;
		cin >> value;
		vec.push_back(value);
	}

	quicksort(vec, 0, vec.size() - 1);
	cout << vec[0];
	for (int i = 1; i < vec.size(); i++)
	{
		cout << " " << vec[i];
	}
	cout << endl;
	return 0;
}