#include<iostream>
using namespace std;

void shellSort(int a[], int n) {
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            for (int j = i - gap; j >= 0 && a[j] > a[j + gap]; j -= gap) {
                swap(a[j], a[j + gap]);
            }
        }
    }
}

int main()
{
    int N;
    std::cin >> N;
    int* array = (int*) malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) {
        std::cin >> array[i];
    }
    shellSort(array, N);
    for (int i = 0; i < N; i++) {
        std::cout << array[i];
        if (i != (N - 1)) std::cout << " ";
        else std::cout << std::endl;
    }
    return 0;
}