#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip>

void count_sort(int*& arr, int len) {
    int rank[len] = {0,};
    for (int i = 0; i < len; ++i) {
        for (int j = 0; j < i; ++j) {
            if (arr[i] >= arr[j])
                ++rank[i];
            else
                ++rank[j];
        }
    } 
    int *temp = new int[len];
    for (int i = 0; i < len; ++i) {
        std::cout << std::setw(2) << rank[i] << " ";
        temp[rank[i]] = arr[i];
    }
    std::cout << std::endl;
    delete [] arr;
    arr = temp;
}


int main() {

    srand(time(nullptr));
    int *arr = new int[10] {0,};
    for (int i = 0; i < 10; ++i) {
        arr[i] = rand() % 100;
    }
    for (int i = 0; i < 10; ++i) {
        std::cout << std::setw(2) << arr[i] << " ";
    }
    std::cout << std::endl;

    count_sort(arr, 10);

    for (int i = 0; i < 10; ++i)
        std::cout << std::setw(2) << arr[i] << " ";
    std::cout << std::endl;

    return 0;
}