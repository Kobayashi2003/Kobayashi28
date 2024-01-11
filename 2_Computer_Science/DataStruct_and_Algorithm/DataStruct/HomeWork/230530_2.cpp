#include<iostream>
using namespace std;

void Merge(int arr[], int low, int mid, int high) {
    // low是第一个有序区的第一个元素，i指向它。
    // mid是第一个有序区的最后一个元素。
    int i = low, j = mid + 1, k = 0; // mid+1是第二个有序区的第一个元素，j指向它。
    int* temp = new(nothrow) int[high - low + 1]; // temp数组暂时存放合并后的有序序列。
    if (!temp) { // 内存分配失败。
        cout << "error";
        return;
    }

    while (i <= mid && j <= high) {
        if (arr[i] <= arr[j])
            temp[k++] = arr[i++]; 
        else
            temp[k++] = arr[j++];
    }
    while (i <= mid)
        temp[k++] = arr[i++];
    while (j <= high)
        temp[k++] = arr[j++];

    for (i = low, k = 0; i <= high; ++i, ++k)
        arr[i] = temp[k];

    delete[]temp; // 删除指针。由于它指向数组，必须使用delete[]。
}

// 利用分治法通过递归实现归并排序。
void MergeSort(int arr[], int low, int high) {
    if (low < high) {
        int mid = (low + high) / 2;
        MergeSort(arr, low, mid);
        MergeSort(arr, mid + 1, high);
        Merge(arr, low, mid, high); 
    }
}

int main(int argc, char* argv[]) {
    int num;
    cin >> num;
    int* a = (int*)malloc(sizeof(int) * num);
    //int a[num];
    for (int i = 0; i < num; i++) {
        cin >> a[i];
    }

    MergeSort(a, 0, num - 1);
    for (int i = 0; i < num; i++) {
        cout << a[i] << " ";
    }

    return 0;
} 