#include <stdio.h>
#include<iostream>
#include <vector>
using namespace std;

template<typename T>
void InsertSort(vector<T> &a, int n) {
    for ( int i = 1; i < n; ++i) {
        T temp = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > temp) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = temp;
    }
} 

int main() {
    vector<int> vec;
    int temp;
    while (cin >> temp) {
        vec.push_back(temp);
        if (cin.get() == '\n')
        break;
    }

    InsertSort(vec, vec.size());
    cout << vec[0];
    for (int i = 1; i < vec.size(); i++)
    {
        cout << " " << vec[i];
    }
    cout << endl;
    //return 0;
}